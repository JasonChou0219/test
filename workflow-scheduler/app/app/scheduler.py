import queue
import os
import time
import logging
import docker
from dataclasses import dataclass
from copy import deepcopy
from datetime import datetime
from enum import IntEnum
from threading import Thread
from typing import Optional
from uuid import UUID
from fastapi.encoders import jsonable_encoder

from app import crud
from app import models
from app.api import deps
from app.schemas import ScheduledJob, ScheduledJobUpdate
from app.models import ScheduledJob
from app.util import docker_helper
from app.util.data_directories import TEMP_DIRECTORY

from apscheduler import events
from apscheduler.schedulers.background import BackgroundScheduler
from influxdb import InfluxDBClient
from requests import get


class ProcessStatusEventType(IntEnum):
    STARTED = 0
    FINISHED_SUCCESSFUL = 1
    FINISHED_MANUALLY = 2
    ERROR = 3


@dataclass
class ProcessStatusEvent:
    job_id: int
    event_type: ProcessStatusEventType
    message: Optional[str] = None


class JobStatus(IntEnum):
    WAITING_FOR_EXECUTION = 0
    SUBMITTED_FOR_EXECUTION = 1
    RUNNING = 2
    FINISHED_SUCCESSFUL = 3
    FINISHED_ERROR = 4
    FINISHED_MANUALLY = 5
    UNKNOWN = 6


@dataclass
class JobState:
    job_id: int
    title: str
    scheduled_job_id: int
    job_template_id:int
    container_id: str
    start_time: datetime
    # end_time: int
    status: JobStatus
    # logs: deque


event_queue = queue.SimpleQueue()
process_status_queue = queue.SimpleQueue()
scheduler = BackgroundScheduler()

job_id_to_data_acquisition_job = {}

scheduled_jobs = {}  # Scheduled Jobs that are stored as scheduled jobs
submitted_jobs = {}  # Scheduled jobs that are submitted to the scheduler
db = next(deps.get_db())
docker_client = docker.from_env()
image_name = 'workflow_executor_python'

def event_listener(event):
    event_queue.put(event)


def change_job_status(job_id: int, status: JobStatus):
    scheduled_jobs[job_id].status = status
    original_scheduled_job = crud.scheduled_job.get(db=db, id=job_id)
    updated_scheduled_job = deepcopy(original_scheduled_job)
    updated_scheduled_job.id = scheduled_jobs[job_id].job_id
    updated_scheduled_job.job_id = scheduled_jobs[job_id].job_template_id
    updated_scheduled_job.job_status = scheduled_jobs[job_id].status
    crud.scheduled_job.update(db=db, db_obj=original_scheduled_job, obj_in=jsonable_encoder(updated_scheduled_job))
    logging.info('Successfully updated ScheduledJob Status')


def start_job(job: ScheduledJob, status_queue: queue.SimpleQueue):
    # devices = [
    #     asdict(get_device_info(booking.device)) for booking in exp.deviceBookings
    # ]
    logging.info(f'Starting job {job.title}')
    logging.info(f'Scanning for workflows')

    for protocol_and_database in job.list_protocol_and_database:
        protocol = protocol_and_database[0]
        database = protocol_and_database[1]

        interval_to_properties_and_commands = {}

        # TODO meta
        # TODO observables
        for feature in protocol.service.features:
            for command in feature.commands:
                if not command.observable and not command.meta:
                    if command.interval not in interval_to_properties_and_commands.keys():
                        interval_to_properties_and_commands[command.interval] = []
                    interval_to_properties_and_commands[command.interval].append((command, feature.identifier))
            for property in feature.properties:
                if not property.observable and not property.meta:
                    if property.interval not in interval_to_properties_and_commands.keys():
                        interval_to_properties_and_commands[property.interval] = []
                    interval_to_properties_and_commands[property.interval].append((property, feature.identifier))

        for interval in interval_to_properties_and_commands.keys():
            apscheduler_job = scheduler.add_job(save_data,
                                                'interval',
                                                seconds=interval,
                                                args=[interval_to_properties_and_commands[interval], protocol.service.uuid, database])
            apscheduler_job.resume()
            if job.id not in job_id_to_data_acquisition_job:
                job_id_to_data_acquisition_job[job.id] = []
            job_id_to_data_acquisition_job[job.id].append(apscheduler_job)

    job_workflows = []
    if job.workflows:
        if job.workflows != None:
            for workflow_info in job.workflows:
                workflow = crud.workflow.get(db=next(deps.get_db()), id=workflow_info[0], job_id=job.job_id)
                logging.info(f'Added workflow {workflow.id} with title {workflow.title} and type {workflow.workflow_type}')
                job_workflows.append(workflow)  # Owner is the job!

            # Todo: Implement the request to get all workflows related to a job and query the respective workflow from the database
            # Todo: Depending on workflow_type, change the executor that it is pushed to!
            # --> #
            logging.info('Starting for loop over workflows')
            for workflow in job_workflows:
                if workflow.workflow_type == 'python':
                    # Todo: Implement a check for start_time of the workflow here.
                    #  The workflow start time may deviate from the job start time
                    services = 'None'
                    container_name = job.title + '_' + str(job.id) + '-' + workflow.title + '_' + str(workflow.id)
                    container = docker_helper.create_python_workflow_container(
                        docker_client,
                        image_name,
                        container_name,
                        workflow.data,
                        f'services={services}'
                    )
                    logging.info(f'Created docker container for job workflow {workflow.id}: \"{container.name}\"')

                    output_thread = Thread(target=print_container_output, args=(container, workflow.id,), daemon=True)
                    wait_thread = Thread(target=wait_until_container_stops,
                                         args=(container, job.id, status_queue))
                    # Todo: Change job id to workflow id. Track job status and workflow status separately
                    # Starting threads
                    container.start()
                    output_thread.start()
                    wait_thread.start()

                    status_queue.put(
                        ProcessStatusEvent(job.id, ProcessStatusEventType.STARTED,
                                           container.id))
                    logging.info(f'Successfully started python executor container: {container}')
                elif workflow.workflow_type == 'node-red':
                    # Todo: Implement a check for start_time of the workflow here.
                    #  The workflow start time may deviate from the job start time
                    logging.info('Starting a node-red container')
                    container = docker_helper.create_node_red_executor_container(workflow.data)
                    logging.info(f'Created docker container for job workflow {workflow.id}: \"{container.name}\"')
                    # output_thread = Thread(target=print_container_output, args=(container, job.id, ), daemon=True)
                    wait_thread = Thread(target=wait_until_container_stops,
                                         args=(container, job.id, status_queue))
                    # Starting threads
                    # output_thread.start()
                    wait_thread.start()

                    status_queue.put(
                        ProcessStatusEvent(workflow.id, ProcessStatusEventType.STARTED,
                                           container.id))
                    pass
                else:
                    pass
        else:
            logging.warning(f'Job {job.title} does not have any attached workflow!')
    return


def wait_until_container_stops(container, job_id: int,
                               status_queue: queue.SimpleQueue):
    status = container.wait()
    logging.info(f'container stopped with StatusCode {status["StatusCode"]}')
    if status['StatusCode'] == 0:
        status_queue.put(
            ProcessStatusEvent(job_id,
                               ProcessStatusEventType.FINISHED_SUCCESSFUL))
    else:
        status_queue.put(
            ProcessStatusEvent(job_id, ProcessStatusEventType.ERROR))
    # Todo: Uncomment the following line once stable
    # container.remove()


def print_container_output(container, workflow_id):
    # container_output = container.attach(logs=False, stream=True)
    container_output = container.logs(follow=True, timestamps=True, stream=True, stdout=True, stderr=True)
    logging.info('Output thread started!')
    log_path = os.path.join(TEMP_DIRECTORY, 'container', f'{datetime.now().strftime("%d_%m_%Y-%H_%M_%S")}_{str(workflow_id)}.log')
    with open(log_path, "w") as file:
        for line in container_output:
            file.write(line.decode())
            # json.dump(line.decode(), file)
            # forward_experiment_log(experiment_id=experiment_id, logging_message=line.decode())


def handle_process_status_events(event: ProcessStatusEvent):
    if event.event_type == ProcessStatusEventType.STARTED:
        scheduled_jobs[event.job_id].container_id = event.message
        change_job_status(event.job_id, JobStatus.RUNNING)
        logging.info(f'{scheduled_jobs[event.job_id].title} started')
    elif event.event_type == ProcessStatusEventType.FINISHED_SUCCESSFUL:
        change_job_status(event.job_id,
                          JobStatus.FINISHED_SUCCESSFUL)
        logging.info(f'{scheduled_jobs[event.job_id].title} finished successful')
    elif event.event_type == ProcessStatusEventType.ERROR:
        change_job_status(event.job_id,
                          JobStatus.FINISHED_ERROR)
        logging.info(f'{scheduled_jobs[event.job_id].title} Error')


def handle_scheduling_jobs(event):
    logging.info('2 submitted_jobs')
    logging.info(submitted_jobs)
    if event.code == events.EVENT_JOB_SUBMITTED:
        if event.job_id in submitted_jobs:
            job_id = submitted_jobs[event.job_id]
            job_entry = scheduled_jobs[job_id]
            change_job_status(job_id, JobStatus.SUBMITTED_FOR_EXECUTION)
            logging.info(f'{job_entry.title} submitted')
    elif event.code == events.EVENT_JOB_REMOVED:
        if event.job_id in submitted_jobs:
            job_entry = scheduled_jobs[submitted_jobs[event.job_id]]
            logging.info(f'{job_entry.title} removed')
    elif event.code == events.EVENT_JOB_ERROR:
        if event.job_id in submitted_jobs:
            job_id = submitted_jobs[event.job_id]
            job_entry = scheduled_jobs[job_id]
            change_job_status(job_id,
                              JobStatus.FINISHED_ERROR)
            logging.info(f'scheduling error for {job_entry.title}')
    elif event.code == events.EVENT_JOB_MISSED:
        if event.job_id in submitted_jobs:
            job_id = submitted_jobs[event.job_id]
            job_entry = scheduled_jobs[job_id]
            change_job_status(job_id,
                              JobStatus.FINISHED_ERROR)
            logging.info(f'job {job_entry.title} missed')


def schedule_future_jobs_from_database():
    scheduled_jobs_from_db = crud.scheduled_job.get_multi(db)
    if len(scheduled_jobs_from_db) > 0:
        for scheduled_job in scheduled_jobs_from_db:
            schedule_job(scheduled_job)


def schedule_job(job: ScheduledJob):
    if job.id not in scheduled_jobs:  # or (
            # scheduled_jobs[job.id].status == JobStatus.FINISHED_ERROR or
            # scheduled_jobs[job.id].status == JobStatus.FINISHED_SUCCESSFUL or
            # scheduled_jobs[job.id].status == JobStatus.FINISHED_MANUALLY):
        scheduled_job = scheduler.add_job(start_job,
                                          'date',
                                          args=[job, process_status_queue],
                                          name=f'job: {job.title}',
                                          run_date=job.execute_at)
        scheduled_jobs[job.id] = \
            JobState(
                job_id=job.id,
                title=job.title,
                scheduled_job_id=scheduled_job.id,
                job_template_id=job.job_id,
                container_id='0',
                start_time=job.created_at,
                status=JobStatus.WAITING_FOR_EXECUTION)
        submitted_jobs[scheduled_job.id] = job.id
        change_job_status(job.id, JobStatus.WAITING_FOR_EXECUTION)


def schedule_job_now(job: ScheduledJob):
    if (job.id in scheduled_jobs) and (
            scheduled_jobs[job.id].status != JobStatus.FINISHED_ERROR or
            scheduled_jobs[job.id].status != JobStatus.FINISHED_SUCCESSFUL or
            scheduled_jobs[job.id].status != JobStatus.FINISHED_MANUALLY):
        pass
        # stop_experiment(job.id)
    scheduled_job = scheduler.add_job(start_job,
                                      args=[job, process_status_queue],
                                      name=f'job: {job.title}')
    scheduled_jobs[job.id] = JobState(
        job_id=job.id,
        title=job.title,
        scheduled_job_id=scheduled_job.id,
        container_id='',
        job_template_id=job.job_id,
        start_time=job.execute_at,
        status=JobStatus.WAITING_FOR_EXECUTION)
    submitted_jobs[job.id] = job.id
    change_job_status(job.id, JobStatus.WAITING_FOR_EXECUTION)


def save_data(properties_and_commands, service_uuid, database):
    for property_or_command in properties_and_commands:
        if isinstance(property_or_command[0], models.Command):
            # TODO make parameters dict of identifier and value
            parameters = []
            for parameter in property_or_command[0].parameters:
                parameters.append(parameter.value)
            responses = []
            for response in property_or_command[0].responses:
                responses.append(response.identifier)

            # TODO route from settings
            response = get("http://service-manager:82/api/v1/sm_functions/unobservable",
                           params=dict({'service_uuid': service_uuid,
                                        'feature_identifier': property_or_command[1],
                                        'function_identifier': property_or_command[0].identifier,
                                        'is_property': False,
                                        'response_identifiers': responses,
                                        'parameters': parameters}))

        else:
            # TODO route from settings
            response = get("http://service-manager:82/api/v1/sm_functions/unobservable",
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
            tags = {'service': service_uuid, 'feature': property_or_command[1], 'command': property_or_command[0].identifier}
            point['measurement'] = 'data-acquisition'
            point['tags'] = tags
            point['time'] = datetime.now()

            if not response:
                point['fields'] = response.json()['detail']
            else:
                point['fields'] = response.json()['response']

            points = [point]

            client.write_points(points)
        except Exception as e:
            print(e)


def stop_data_acquisition_for_job(job_id: int):
    if job_id in job_id_to_data_acquisition_job.keys():
        for job in job_id_to_data_acquisition_job[job_id]:
            job.remove()
        del job_id_to_data_acquisition_job[job_id]


def main():
    image = docker_helper.create_python_workflow_image(docker_client, image_name)
    scheduler.start()
    scheduler.add_listener(event_listener, events.EVENT_ALL)
    schedule_future_jobs_from_database()
    t = time.time()
    try:
        while True:
            try:
                handle_scheduling_jobs(event_queue.get_nowait())
            except queue.Empty:
                pass

            try:
                handle_process_status_events(process_status_queue.get_nowait())
            except queue.Empty:
                pass

            # receive_and_execute_commands()
            t2 = time.time()
            if t2 - t >= 5:
                t = t2
                schedule_future_jobs_from_database()
    except KeyboardInterrupt:
        pass
    finally:
        scheduler.shutdown()


if __name__ == '__main__':
    main()
