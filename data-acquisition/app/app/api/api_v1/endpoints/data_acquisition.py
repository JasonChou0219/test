import json
from datetime import datetime
from typing import List, Tuple, Any

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from fastapi import Request, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from influxdb import InfluxDBClient
from requests import post
from sqlalchemy.orm import Session
import asyncio
import websockets
import logging

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

scheduler = BackgroundScheduler(job_defaults={'max_instances': 100},
                                executors={'default': ThreadPoolExecutor(100), 'processpool': ProcessPoolExecutor(100)})
scheduler.start()

job_id_to_data_acquisition_job = {}

@router.post("/{job_id}/start", response_model=None)
def start_data_acquisition_for_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        job_id: int,
        owner_id: int,
        list_protocol_and_database: List[Tuple[schemas.Protocol, schemas.Database]],
) -> Any:
    """
    Start data-acquisition for job specified by id.
    """
    for protocol_and_database in list_protocol_and_database:
        protocol = protocol_and_database[0]
        database = protocol_and_database[1]

        interval_to_non_meta_and_unobservable_properties_and_commands = {}
        non_meta_and_observable_commands_and_properties = []
        meta_and_unobservable_commands_and_properties = []
        meta_and_observable_commands = []
        meta_and_observable_properties = []

        for feature in protocol.service.features:
            # Separate commands into meta and unobservable, meta and observable, non-meta and observable,
            # non-meta and unobservable
            for command in feature.commands:
                if command.meta:
                    if not command.observable:
                        meta_and_unobservable_commands_and_properties.append((command, feature.identifier))
                    else:
                        meta_and_observable_commands.append((command, feature.identifier))
                elif command.observable:
                    non_meta_and_observable_commands_and_properties.append((command, feature.identifier))
                else:
                    if command.interval not in interval_to_non_meta_and_unobservable_properties_and_commands.keys():
                        interval_to_non_meta_and_unobservable_properties_and_commands[command.interval] = []
                    interval_to_non_meta_and_unobservable_properties_and_commands[command.interval].append((command, feature.identifier))
            for property in feature.properties:
                # Separate properties into meta and unobservable, meta and observable, non-meta and observable,
                # non-meta and unobservable
                if property.meta:
                    if not property.observable:
                        meta_and_unobservable_commands_and_properties.append((property, feature.identifier))
                    else:
                        meta_and_observable_properties.append((property, feature.identifier))
                elif property.observable:
                    non_meta_and_observable_commands_and_properties.append((property, feature.identifier))
                else:
                    if property.interval not in interval_to_non_meta_and_unobservable_properties_and_commands.keys():
                        interval_to_non_meta_and_unobservable_properties_and_commands[property.interval] = []
                    interval_to_non_meta_and_unobservable_properties_and_commands[property.interval].append((property, feature.identifier))

        # Run data acquisition for non-meta unobservable commands and properties
        for interval in interval_to_non_meta_and_unobservable_properties_and_commands.keys():
            apscheduler_job = scheduler.add_job(save_unobservable_data,
                                                'interval',
                                                seconds=interval,
                                                args=[interval_to_non_meta_and_unobservable_properties_and_commands[interval], job_id, protocol.id, protocol.service.uuid, owner_id, database])
            apscheduler_job.modify(next_run_time=datetime.now())
            if job_id not in job_id_to_data_acquisition_job:
                job_id_to_data_acquisition_job[job_id] = []
            job_id_to_data_acquisition_job[job_id].append(apscheduler_job)

        # Run data acquisition for meta unobservable commands and properties
        scheduler.add_job(save_unobservable_data,
                          args=[meta_and_unobservable_commands_and_properties, job_id, protocol.id, protocol.service.uuid, owner_id, database])

        # Run data acquisition for non-meta observable commands and properties
#        scheduler.add_job(save_observable_data,
#                          args=[non_meta_and_observable_commands_and_properties, job_id, protocol.id, protocol.service.uuid, owner_id, database])

        # Run data acquisition for meta observable properties
        scheduler.add_job(save_unobservable_data,
                          args=[meta_and_observable_properties, job_id, protocol.id, protocol.service.uuid, owner_id, database])

        # Run data acquisition for meta observable commands
#        scheduler.add_job(save_meta_observable_command_data,
#                          args=[meta_and_observable_commands, job_id, protocol.id, protocol.service.uuid, owner_id, database])

        # Save custom data
        scheduler.add_job(save_custom_data,
                          args=[protocol.custom_data, job_id, protocol.id, owner_id, database])

    return


def save_unobservable_data(properties_and_commands, job_id, protocol_id, service_uuid, owner_id, database):
    for property_or_command in properties_and_commands:
        parameters = {}
        if isinstance(property_or_command[0], schemas.Command):
            for parameter in property_or_command[0].parameters:
                parameters[parameter.identifier] = parameter.value
            # Convert parameters to appropriate types
            for parameter_name in parameters.keys():
                if str(parameters[parameter_name]).lower() in ["true", "false"]:
                    parameters[parameter_name] = True if str(parameters[parameter_name]).lower() == "true" else False
                if str(parameters[parameter_name]).isdecimal():  # Floats are not supported by REST query parameters
                    parameters[parameter_name] = int(parameters[parameter_name])
            responses = []
            for response in property_or_command[0].responses:
                responses.append(response.identifier)

            response = post("http://service-manager:82/api/v1/sm_functions/unobservable",
                            params=dict({'service_uuid': service_uuid,
                                         'feature_identifier': property_or_command[1],
                                         'function_identifier': property_or_command[0].identifier,
                                         'is_property': False,
                                         'response_identifiers': responses}),
                            json=jsonable_encoder(parameters))

        else:
            response = post("http://service-manager:82/api/v1/sm_functions/unobservable",
                            params=dict({'service_uuid': service_uuid,
                                         'feature_identifier': property_or_command[1],
                                         'function_identifier': property_or_command[0].identifier,
                                         'is_property': True}))

        try:
            client = InfluxDBClient(host=database.address,
                                    port=database.port,
                                    username=database.username,
                                    password=database.password,
                                    database=database.name)
            client.create_database(database.name)
            if isinstance(property_or_command[0], schemas.Command):
                tags = {'job': job_id, 'protocol': protocol_id, 'service': service_uuid,
                        'feature': property_or_command[1], 'command': property_or_command[0].identifier,
                        'owner': owner_id, 'parameters': parameters}
            else:
                tags = {'job': job_id, 'protocol': protocol_id, 'service': service_uuid, 'feature': property_or_command[1], 'property': property_or_command[0].identifier, 'owner': owner_id}

            if not response:
                response = {'error': response.json()['detail']}
            else:
                response = response.json()['response']
            point = [{
                "measurement": "data_acquisition",
                "tags": tags,
                "time": datetime.now(),
                "fields": response
            }]

            client.write_points(point, retention_policy=database.retention_policy)
        except Exception as e:
            logging.info(e)


def save_observable_data(properties_and_commands, job_id, protocol_id, service_uuid, owner_id, database):
    for property_or_command in properties_and_commands:
        parameters = {}
        if isinstance(property_or_command[0], schemas.Command):
            for parameter in property_or_command[0].parameters:
                parameters[parameter.identifier] = parameter.value
            # Convert parameters to appropriate types
            for parameter_name in parameters.keys():
                if str(parameters[parameter_name]).lower() in ["true", "false"]:
                    parameters[parameter_name] = True if str(parameters[parameter_name]).lower() == "true" else False
                if str(parameters[parameter_name]).isdecimal():  # Floats are not supported by REST query parameters
                    parameters[parameter_name] = int(parameters[parameter_name])

            response = post("http://service-manager:82/api/v1/sm_functions/observable",
                            params=dict({'service_uuid': service_uuid,
                                         'feature_identifier': property_or_command[1],
                                         'function_identifier': property_or_command[0].identifier}),
                            json=jsonable_encoder(parameters))

        else:
            response = post("http://service-manager:82/api/v1/sm_functions/unobservable",
                            params=dict({'service_uuid': service_uuid,
                                         'feature_identifier': property_or_command[1],
                                         'function_identifier': property_or_command[0].identifier,
                                         'is_property': True}))
        try:
            client = InfluxDBClient(host=database.address,
                                    port=database.port,
                                    username=database.username,
                                    password=database.password,
                                    database=database.name)
            client.create_database(database.name)
            if isinstance(property_or_command[0], schemas.Command):
                tags = {'job': job_id, 'protocol': protocol_id, 'service': service_uuid,
                        'feature': property_or_command[1], 'command': property_or_command[0].identifier,
                        'owner': owner_id, 'parameters': parameters}
            else:
                tags = {'job': job_id, 'protocol': protocol_id, 'service': service_uuid,
                        'feature': property_or_command[1], 'property': property_or_command[0].identifier,
                        'owner': owner_id}
            point = [{
                "measurement": "data_acquisition",
                "tags": tags,
                "time": datetime.now(),
                "fields": {}
            }]
            if not response:
                point[0]['fields'] = response = {'error': response.json()['detail']}
                client.write_points(point, retention_policy=database.retention_policy)
            else:
                websocket_uuid = response.json()
                scheduler.add_job(start_websocket_handling, args=[websocket_uuid, client, point, database.retention_policy])
        except Exception as e:
            logging.info(e)


def start_websocket_handling(websocket_uuid, client, point, retention_policy):
    asyncio.run(handle_websocket_data(websocket_uuid, client, point, retention_policy))


async def handle_websocket_data(websocket_uuid, client, point, retention_policy):
    async with websockets.connect("ws://service-manager:82/api/v1/sm_functions/ws/observable/" + websocket_uuid) as websocket:
        await websocket.send(websocket_uuid)
        async for message in websocket:
            message_as_json = json.loads(message)
            if message_as_json[next(iter(message_as_json))]['intermediate_response'] is not None:
                point[0]['tags']['is_intermediate_response'] = True
                point[0]['fields'] = message_as_json[next(iter(message_as_json))]['intermediate_response']
            else:
                point[0]['tags']['is_intermediate_response'] = False
                point[0]['fields'] = message_as_json[next(iter(message_as_json))]['response']
            client.write_points(point, retention_policy=retention_policy)


def save_custom_data(custom_data, job_id, protocol_id, owner_id, database):
    try:
        client = InfluxDBClient(host=database.address,
                                port=database.port,
                                username=database.username,
                                password=database.password,
                                database=database.name)
        client.create_database(database.name)
        tags = {'job': job_id, 'protocol': protocol_id, 'owner': owner_id}
        point = [{
            "measurement": "data_acquisition",
            "tags": tags,
            "time": datetime.now(),
            "fields": custom_data
        }]

        client.write_points(point, retention_policy=database.retention_policy)
    except Exception as e:
        logging.info(e)


def save_meta_observable_command_data(commands, job_id, protocol_id, service_uuid, owner_id, database):
    for command in commands:
        parameters = {}
        for parameter in command[0].parameters:
            parameters[parameter.identifier] = parameter.value
        # Convert parameters to appropriate types
        for parameter_name in parameters.keys():
            if str(parameters[parameter_name]).lower() in ["true", "false"]:
                parameters[parameter_name] = True if str(parameters[parameter_name]).lower() == "true" else False
            if str(parameters[parameter_name]).isdecimal():  # Floats are not supported by REST query parameters
                parameters[parameter_name] = int(parameters[parameter_name])

        response = post("http://service-manager:82/api/v1/sm_functions/observable",
                        params=dict({'service_uuid': service_uuid,
                                     'feature_identifier': command[1],
                                     'function_identifier': command[0].identifier}),
                        json=jsonable_encoder(parameters))

        try:
            client = InfluxDBClient(host=database.address,
                                    port=database.port,
                                    username=database.username,
                                    password=database.password,
                                    database=database.name)
            client.create_database(database.name)
            tags = {'job': job_id, 'protocol': protocol_id, 'service': service_uuid, 'feature': command[1], 'command': command[0].identifier, 'owner': owner_id, 'parameters': parameters}
            point = [{
                "measurement": "data_acquisition",
                "tags": tags,
                "time": datetime.now(),
                "fields": {}
            }]

            if not response:
                point[0]['fields'] = {'error': response.json()['detail']}
                client.write_points(point, retention_policy=database.retention_policy)
            else:
                websocket_uuid = response.json()
                scheduler.add_job(start_websocket_handling_for_meta_observable_command, args=[websocket_uuid, client, point, database.retention_policy])
        except Exception as e:
            logging.info(e)


def start_websocket_handling_for_meta_observable_command(websocket_uuid, client, point, retention_policy):
    asyncio.run(handle_websocket_data_meta_observable_command(websocket_uuid, client, point, retention_policy))


async def handle_websocket_data_meta_observable_command(websocket_uuid, client, point, retention_policy):
    async with websockets.connect("ws://service-manager:82/api/v1/sm_functions/ws/observable/" + websocket_uuid) as websocket:
        await websocket.send(websocket_uuid)
        async for message in websocket:
            message_as_json = json.loads(message)
            if message_as_json[next(iter(message_as_json))]['intermediate_response'] is not None:
                point[0]['tags']['is_intermediate_response'] = True
                point[0]['fields'] = message_as_json[next(iter(message_as_json))]['intermediate_response']
            else:
                point[0]['tags']['is_intermediate_response'] = False
                point[0]['fields'] = message_as_json[next(iter(message_as_json))]['response']
            await websocket.close()
            client.write_points(point, retention_policy=retention_policy)


@router.get("/{job_id}/stop_data_acquisition", response_model=None)
def stop_data_acquisition_for_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        job_id: int,
) -> Any:
    """
    Stop data acquisition for job specified by id.
    """
    if job_id in job_id_to_data_acquisition_job.keys():
        for job in job_id_to_data_acquisition_job[job_id]:
            job.remove()
        del job_id_to_data_acquisition_job[job_id]

    return
