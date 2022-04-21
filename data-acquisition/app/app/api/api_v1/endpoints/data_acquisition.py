from datetime import datetime
from typing import List, Tuple, Any

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import Request, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from influxdb import InfluxDBClient
from requests import post
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

scheduler = BackgroundScheduler()
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
        meta_and_observable_commands_and_properties = []

        # TODO observables
        for feature in protocol.service.features:
            # Separate commands into meta and unobservable, meta and observable, non-meta and observable, non-meta and unobservable
            for command in feature.commands:
                if command.meta:
                    if not command.observable:
                        meta_and_unobservable_commands_and_properties.append((command, feature.identifier))
                    else:
                        meta_and_observable_commands_and_properties.append((command, feature.identifier))
                elif command.observable:
                    non_meta_and_observable_commands_and_properties.append((command, feature.identifier))
                else:
                    if command.interval not in interval_to_non_meta_and_unobservable_properties_and_commands.keys():
                        interval_to_non_meta_and_unobservable_properties_and_commands[command.interval] = []
                    interval_to_non_meta_and_unobservable_properties_and_commands[command.interval].append((command, feature.identifier))
            for property in feature.properties:
                # Separate properties into meta and unobservable, meta and observable, non-meta and observable, non-meta and unobservable
                if property.meta:
                    if not property.observable:
                        meta_and_unobservable_commands_and_properties.append((property, feature.identifier))
                    else:
                        meta_and_observable_commands_and_properties.append((property, feature.identifier))
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

            # TODO route from settings
            response = post("http://service-manager:82/api/v1/sm_functions/unobservable",
                            params=dict({'service_uuid': service_uuid,
                                         'feature_identifier': property_or_command[1],
                                         'function_identifier': property_or_command[0].identifier,
                                         'is_property': False,
                                         'response_identifiers': responses}),
                            json=jsonable_encoder(parameters))

        else:
            # TODO route from settings
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
            point = {}
            if isinstance(property_or_command[0], schemas.Command):
                tags = {'job': job_id, 'protocol': protocol_id, 'service': service_uuid, 'feature': property_or_command[1], 'command': property_or_command[0].identifier, 'owner': owner_id, 'parameters': parameters}
            else:
                tags = {'job': job_id, 'protocol': protocol_id, 'service': service_uuid, 'feature': property_or_command[1], 'property': property_or_command[0].identifier, 'owner': owner_id}
            point['measurement'] = 'data-acquisition'
            point['tags'] = tags
            point['time'] = datetime.now()

            if not response:
                point['fields'] = {'error': response.json()['detail']}
            else:
                point['fields'] = response.json()['response']

            points = [point]

            client.write_points(points, retention_policy=database.retention_policy)
        except Exception as e:
            print(e)


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

            # TODO route from settings
            response = post("http://service-manager:82/api/v1/sm_functions/observable",
                            params=dict({'service_uuid': service_uuid,
                                         'feature_identifier': property_or_command[1],
                                         'function_identifier': property_or_command[0].identifier}),
                            json=jsonable_encoder(parameters))

        else:
            return
            # TODO route from settings
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
            point = {}
            if isinstance(property_or_command[0], schemas.Command):
                tags = {'job': job_id, 'protocol': protocol_id, 'service': service_uuid, 'feature': property_or_command[1], 'command': property_or_command[0].identifier, 'owner': owner_id, 'parameters': parameters}
            else:
                tags = {'job': job_id, 'protocol': protocol_id, 'service': service_uuid, 'feature': property_or_command[1], 'property': property_or_command[0].identifier, 'owner': owner_id}
            point['measurement'] = 'data-acquisition'
            point['tags'] = tags
            point['time'] = datetime.now()

            if not response:
                point['fields'] = {'error': response.json()['detail']}
                points = [point]
                client.write_points(points, retention_policy=database.retention_policy)
            else:
                websocket_uuid = response.json()
                # receive data from websocket and save it to database
        except Exception as e:
            print(e)


def save_custom_data(custom_data, job_id, protocol_id, owner_id, database):
    try:
        client = InfluxDBClient(host=database.address,
                                port=database.port,
                                username=database.username,
                                password=database.password,
                                database=database.name)
        client.create_database(database.name)
        point = {}
        tags = {'job': job_id, 'protocol': protocol_id, 'owner': owner_id}
        point['measurement'] = 'data-acquisition'
        point['tags'] = tags
        point['time'] = datetime.now()

        point['fields'] = custom_data

        points = [point]

        client.write_points(points, retention_policy=database.retention_policy)
    except Exception as e:
        print(e)


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
