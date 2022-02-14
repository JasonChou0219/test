import queue
import time
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from threading import Thread
from typing import Optional
from uuid import UUID
from fastapi.encoders import jsonable_encoder

from app import crud
from app.api import deps
from app.schemas import ScheduledJob
from app.models import ScheduledJob
from app.util import docker_helper

from apscheduler import events
from apscheduler.schedulers.background import BackgroundScheduler


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
    container_id: str
    start_time: datetime
    # end_time: int
    status: JobStatus
    # logs: deque


event_queue = queue.SimpleQueue()
process_status_queue = queue.SimpleQueue()
scheduler = BackgroundScheduler()

scheduled_jobs = {}  # Scheduled Jobs that are stored as scheduled jobs
submitted_jobs = {}  # Scheduled jobs that are submitted to the scheduler
db = next(deps.get_db())

def event_listener(event):
    event_queue.put(event)


def change_job_status(job_id: int, status: JobStatus):

    scheduled_jobs[job_id].job_status = status
    logging.info('Updating ScheduledJob Status')
    original_scheduled_job = crud.scheduled_job.get(db=db, id=job_id)
    scheduled_job = crud.scheduled_job.update(db=db, db_obj=original_scheduled_job, obj_in=jsonable_encoder(scheduled_jobs[job_id]))
    # crud.scheduled_job.update(db=deps.get_db(), db_obj=ScheduledJob, obj_in=scheduled_jobs[job_id])
    logging.info('Successfully updated ScheduledJob Status')


def start_job(job: ScheduledJob, status_queue: queue.SimpleQueue):
    # devices = [
    #     asdict(get_device_info(booking.device)) for booking in exp.deviceBookings
    # ]
    logging.info(f'Starting job {job.title}')
    logging.info(f'Scanning for workflows')
    job_workflows = []
    if job.workflows:
        logging.info('Workflows are:')
        logging.info(job.workflows)
        logging.info(type(job.workflows))
        for workflow in job.workflows:
            logging.info('workflow is:')
            logging.info(workflow[0])
            workflow = crud.workflow.get(db=db, id=workflow[0])
            logging.info(workflow)
            logging.info(f'Added workflow {workflow[0]} with title {workflow[1]}')
            job_workflows.append(workflow)  # Owner is the job!

    # What if workflows empty?

    # Todo: Implement the request to get all workflows related to a job and query the respective workflow from the database
    # Todo: Depending on workflow_type, change the executor that it is pushed to!
    # --> #


    for workflow in workflows:
        if workflow.workflow.type == 'python':
            # Todo: Implement a check for start_time of the workflow here.
            #  The workflow start time may deviate from the job start time
            pass
        elif workflow.workflow.type == 'node-red':
            # Todo: Implement a check for start_time of the workflow here.
            #  The workflow start time may deviate from the job start time
            pass
    # --> #

    container = docker_helper.create_node_red_executor_container(job.flow)
    print(f'Created docker container for job {job.id}: \"{container.name}\"')

    # output_thread = Thread(target=print_container_output, args=(container, job.id, ), daemon=True)
    wait_thread = Thread(target=wait_until_container_stops,
                         args=(container, job.id, status_queue))
    # Starting threads
    # output_thread.start()
    wait_thread.start()

    status_queue.put(
        ProcessStatusEvent(job.id, ProcessStatusEventType.STARTED,
                           container.id))
    return


def wait_until_container_stops(container, job_id: int,
                               status_queue: queue.SimpleQueue):
    status = container.wait()
    print(f'container stopped with StatusCode {status["StatusCode"]}')
    if status['StatusCode'] == 0:
        status_queue.put(
            ProcessStatusEvent(job_id,
                               ProcessStatusEventType.FINISHED_SUCCESSFUL))
    else:
        status_queue.put(
            ProcessStatusEvent(job_id, ProcessStatusEventType.ERROR))
    container.remove()


# def print_container_output(container, experiment_id):
#     # container_output = container.attach(logs=False, stream=True)
#     container_output = container.logs(follow=True, timestamps=True, stream=True, stdout=True, stderr=True)
#     print('Output thread started!')
#     log_path = os.path.join(TEMP_DIRECTORY, 'container', f'{datetime.now().strftime("%d_%m_%Y-%H_%M_%S")}_{str(experiment_id)}.log')
#     with open(log_path, "w") as file:
#         for line in container_output:
#             print(line.decode())
#             file.write(line.decode())
#             # json.dump(line.decode(), file)
#             forward_experiment_log(experiment_id=experiment_id, logging_message=line.decode())


def handle_process_status_events(event: ProcessStatusEvent):
    if event.event_type == ProcessStatusEventType.STARTED:
        scheduled_jobs[event.job_id].container_id = event.message
        change_job_status(event.job_id, JobStatus.RUNNING)
        print(f'{scheduled_jobs[event.job_id].title} started')
    elif event.event_type == ProcessStatusEventType.FINISHED_SUCCESSFUL:
        change_job_status(event.job_id,
                          JobStatus.FINISHED_SUCCESSFUL)
        print(f'{scheduled_jobs[event.job_id].title} finished successful')
    elif event.event_type == ProcessStatusEventType.ERROR:
        change_job_status(event.job_id,
                          JobStatus.FINISHED_ERROR)
        print(f'{scheduled_jobs[event.job_id].title} Error')


def handle_scheduling_jobs(event):
    if event.code == events.EVENT_JOB_SUBMITTED:
        if event.job_id in submitted_jobs:
            job_id = submitted_jobs[event.job_id]
            job_entry = scheduled_jobs[job_id]
            change_job_status(job_id, JobStatus.SUBMITTED_FOR_EXECUTION)
            print(f'{job_entry.title} submitted')
    elif event.code == events.EVENT_JOB_REMOVED:
        if event.job_id in submitted_jobs:
            job_entry = scheduled_jobs[submitted_jobs[event.job_id]]
            print(f'{job_entry.title} removed')
    elif event.code == events.EVENT_JOB_ERROR:
        if event.job_id in submitted_jobs:
            job_id = submitted_jobs[event.job_id]
            job_entry = scheduled_jobs[job_id]
            change_job_status(job_id,
                              JobStatus.FINISHED_ERROR)
            print(f'scheduling error for {job_entry.title}')
    elif event.code == events.EVENT_JOB_MISSED:
        if event.job_id in submitted_jobs:
            job_id = submitted_jobs[event.job_id]
            job_entry = scheduled_jobs[job_id]
            change_job_status(job_id,
                              JobStatus.FINISHED_ERROR)
            print(f'job {job_entry.title} missed')


def schedule_future_jobs_from_database():
    scheduled_jobs_from_db = crud.scheduled_job.get_multi(db)
    if len(scheduled_jobs_from_db) > 0:
        logging.info(f'1. Queried scheduled jobs from database: {scheduled_jobs_from_db[0].workflows}')
        if len(scheduled_jobs_from_db) > 1:
            logging.info(f'2. Queried scheduled jobs from database: {scheduled_jobs_from_db[1].workflows}')
        for scheduled_job in scheduled_jobs_from_db:
            logging.info(scheduled_job)
            schedule_job(scheduled_job)


def schedule_job(job: ScheduledJob):
    if (job.id not in scheduled_jobs) or (
            scheduled_jobs[job.id].status == JobStatus.FINISHED_ERROR or
            scheduled_jobs[job.id].status == JobStatus.FINISHED_SUCCESSFUL or
            scheduled_jobs[job.id].status == JobStatus.FINISHED_MANUALLY):
        scheduled_job = scheduler.add_job(start_job,
                                          'date',
                                          args=[job, process_status_queue],
                                          name=f'job: {job.title}',
                                          run_date=job.execute_at)
        scheduled_jobs[job.id] = \
            JobState(job.id, job.title, scheduled_job.id, '0', job.created_at, JobStatus.WAITING_FOR_EXECUTION)
        submitted_jobs[scheduled_job.id] = job.id
        change_job_status(job.id, JobStatus.WAITING_FOR_EXECUTION)


def schedule_job_now(job: ScheduledJob):
    if (job.id in jobs) and (
            scheduled_jobs[job.id].status != JobStatus.FINISHED_ERROR or
            scheduled_jobs[job.id].status != JobStatus.FINISHED_SUCCESSFUL
            or
            scheduled_jobs[job.id].status != JobStatus.FINISHED_MANUALLY):
        pass
        # stop_experiment(job.id)
    scheduled_job = scheduler.add_job(start_job,
                                      args=[job, process_status_queue],
                                      name=f'job: {job.title}')
    scheduled_jobs[job.id] = JobState(
        job.id, job.title, scheduled_job.id, '0', job.execute_at,
        JobStatus.WAITING_FOR_EXECUTION)
    submitted_jobs[job.id] = job.id
    change_job_status(job.id, JobStatus.WAITING_FOR_EXECUTION)


def main():
    scheduler.start()
    scheduler.add_listener(event_listener, events.EVENT_ALL)
    schedule_future_jobs_from_database()
    t = time.time()
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

    scheduler.shutdown()


if __name__ == '__main__':
    main()
