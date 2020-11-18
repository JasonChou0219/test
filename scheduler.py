#!/bin/env python3
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.job import Job
from apscheduler import events
import time
from datetime import datetime
import source.device_manager.experiment as experiment
from source.device_manager.script import Script, get_user_script
import redis
import msgpack
from dataclasses import dataclass
from enum import IntEnum
import queue
from typing import Optional
import epicbox
import multiprocessing


class ExperimentStatus(IntEnum):
    WAITING_FOR_EXECUTION = 0
    SUBMITED_FOR_EXECUTION = 1
    RUNNING = 2
    FINISHED_SUCCESSFUL = 3
    FINISHED_ERROR = 4
    FINISHED_MANUAL = 5
    UNKNOWN = 6


@dataclass
class ExperimentState:
    experiment_id: int
    name: str
    job_id: int
    process: multiprocessing.Process
    start_time: int
    end_time: int
    status: ExperimentStatus


class ProcessStatusEventType(IntEnum):
    STARTED = 0
    FINISHED_SUCCESSFUL = 1
    ERROR = 3


@dataclass
class ProcessStatusEvent:
    experiment_id: int
    event_type: ProcessStatusEventType
    message: Optional[str] = None


event_queue = queue.SimpleQueue()
process_status_queue = multiprocessing.Queue()

experiments = {}
job_to_experiment = {}

scheduler = BackgroundScheduler()
redis_connection = redis.Redis(host='localhost')
pubsub = redis_connection.pubsub()


def start_experiment(process: multiprocessing.Process):
    process.start()


def run_experiment(experiment_id: int, q: queue.Queue):
    try:
        q.put(ProcessStatusEvent(experiment_id,
                                 ProcessStatusEventType.STARTED))
        exp = experiment.get_experiment(experiment_id)
        script = get_user_script(exp.scriptID)
        epicbox.configure(
            profiles=[epicbox.Profile('python', 'user_script:latest')])
        files = [{'name': script.fileName, 'content': script.data.encode()}]
        #limit memory to 500MB
        limits = {'cputime': None, 'realtime': None, 'memory': 500}
        result = epicbox.run('python',
                             f'python3 {script.fileName}',
                             files=files,
                             limits=limits)
        print(result)
        if result['status_code'] == 0:
            q.put(
                ProcessStatusEvent(experiment_id,
                                   ProcessStatusEventType.FINISHED_SUCCESSFUL))
        else:
            q.put(
                ProcessStatusEvent(experiment_id,
                                   ProcessStatusEventType.ERROR))
    except Exception:
        q.put(ProcessStatusEvent(experiment_id, ProcessStatusEventType.ERROR))
    return


def handle_process_status_events(event: ProcessStatusEvent):
    if event.event_type == ProcessStatusEventType.STARTED:
        experiments[event.experiment_id].status = ExperimentStatus.RUNNING
        print(f'{experiments[event.experiment_id].name} started')
    elif event.event_type == ProcessStatusEventType.FINISHED_SUCCESSFUL:
        experiments[
            event.experiment_id].status = ExperimentStatus.FINISHED_SUCCESSFUL
        print(f'{experiments[event.experiment_id].name} finished successfull')
    elif event.event_type == ProcessStatusEventType.ERROR:
        experiments[
            event.experiment_id].status = ExperimentStatus.FINISHED_ERROR
        print(f'{experiments[event.experiment_id].name} Error')


def event_listener(event):
    event_queue.put(event)


def handle_scheduling_events(event):
    if event.code == events.EVENT_JOB_SUBMITTED:
        if event.job_id in job_to_experiment:
            experiment_entry = experiments[job_to_experiment[event.job_id]]
            experiment_entry.status = ExperimentStatus.SUBMITED_FOR_EXECUTION
            print(f'{experiment_entry.name} submitted')
    elif event.code == events.EVENT_JOB_REMOVED:
        if event.job_id in job_to_experiment:
            experiment_entry = experiments[job_to_experiment[event.job_id]]
            print(f'{experiment_entry.name} removed')
    elif event.code == events.EVENT_JOB_ERROR:
        if event.job_id in job_to_experiment:
            experiment_entry = experiments[job_to_experiment[event.job_id]]
            experiment_entry.status = ExperimentStatus.FINISHED_ERROR
            print('scheduling error')
    elif event.code == events.EVENT_JOB_MISSED:
        if event.job_id in job_to_experiment:
            experiment_entry = experiments[job_to_experiment[event.job_id]]
            experiment_entry.status = ExperimentStatus.FINISHED_ERROR
            print('experiment missed')


def schedule_future_experiments_from_database():
    for exp in experiment.get_scheduling_info():
        schedule_experiment(exp)


def schedule_experiment(exp: experiment.SchedulingInfo):
    if (exp.id not in experiments) or (
            experiments[exp.id].status == ExperimentStatus.FINISHED):
        process = multiprocessing.Process(target=run_experiment,
                                          args=[exp.id, process_status_queue])
        job = scheduler.add_job(start_experiment,
                                'date',
                                args=[process],
                                name=f'experiment:{exp.name}',
                                run_date=datetime.fromtimestamp(exp.start))
        experiments[exp.id] = ExperimentState(
            exp.id, exp.name, job.id, process, exp.start, exp.end,
            ExperimentStatus.WAITING_FOR_EXECUTION)
        job_to_experiment[job.id] = exp.id


def schedule_experiment_now(exp: experiment.SchedulingInfo):
    if (exp.id in experiments) and (experiments[exp.id].status !=
                                    ExperimentStatus.FINISHED):
        stop_experiment(exp.id)

    process = multiprocessing.Process(target=run_experiment,
                                      args=[exp.id, process_status_queue])
    job = scheduler.add_job(start_experiment,
                            args=[process],
                            name=f'experiment:{exp.name}')
    experiments[exp.id] = ExperimentState(
        exp.id, exp.name, job.id, process, exp.start, exp.end,
        ExperimentStatus.WAITING_FOR_EXECUTION)
    job_to_experiment[job.id] = exp.id


def stop_experiment(experiment_id):
    if experiment_id in experiments:
        experiment_entry = experiments[experiment_id]
        if experiment_entry.status == ExperimentStatus.WAITING_FOR_EXECUTION:
            scheduler.remove_job(experiment_entry.job_id)
            experiment_entry.status = ExperimentStatus.FINISHED_MANUAL
        elif experiment_entry.status == ExperimentStatus.RUNNING:
            experiment_entry.process.terminate()
            print('terminate process')
            experiment_entry.status = ExperimentStatus.FINISHED_MANUAL


def get_experiment_status(experiment_id):
    if experiment_id not in experiments:
        return ExperimentStatus.UNKNOWN
    return experiments[experiment_id].status


def receive_and_execute_commands():
    message = pubsub.get_message()
    if (message is None) or (message['type'] != 'message'):
        return

    data = msgpack.unpackb(message['data'], raw=False)
    command = data['command']
    params = data['params']

    if command == 'start':
        print('schedule experiment now')
        exp = experiment.get_experiment(params[0])
        schedule_experiment_now(exp)
    elif command == 'stop':
        print('stop experiment')
        stop_experiment(params[0])


def main():
    pubsub.subscribe('scheduler')
    scheduler.add_listener(event_listener, events.EVENT_ALL)
    scheduler.start()
    schedule_future_experiments_from_database()
    t = time.time()
    while True:
        try:
            handle_scheduling_events(event_queue.get_nowait())
        except queue.Empty:
            pass

        try:
            handle_process_status_events(process_status_queue.get_nowait())
        except queue.Empty:
            pass

        receive_and_execute_commands()
        t2 = time.time()
        if t2 - t >= 5:
            t = t2
            schedule_future_experiments_from_database()

    scheduler.shutdown()


if __name__ == '__main__':
    main()
