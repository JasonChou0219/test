#!/bin/env python3

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.job import Job
from apscheduler import events
import time
from datetime import datetime
import data_handler
import source.device_manager.experiment as experiment
from source.device_manager.experiment import ExperimentStatus
from source.device_manager.device_manager import DeviceManager
from source.device_manager.script import Script, get_user_script
from source.device_manager.device import get_device_info
import redis
import msgpack
from dataclasses import dataclass,asdict
from enum import IntEnum
import queue
from typing import Optional
import docker
import docker_helper
from threading import Thread
import json


@dataclass
class ExperimentState:
    experiment_id: int
    name: str
    job_id: int
    container_id: str
    start_time: int
    end_time: int
    status: ExperimentStatus


class ProcessStatusEventType(IntEnum):
    STARTED = 0
    FINISHED_SUCCESSFUL = 1
    FINISHED_MANUALLY = 2
    ERROR = 3


@dataclass
class ProcessStatusEvent:
    experiment_id: int
    event_type: ProcessStatusEventType
    message: Optional[str] = None


event_queue = queue.SimpleQueue()
process_status_queue = queue.SimpleQueue()

experiments = {}
job_to_experiment = {}
experiment_id_to_data_handler_jobs = {}

scheduler = BackgroundScheduler()
redis_connection = redis.Redis(host='localhost')
pubsub = redis_connection.pubsub()


def change_experiment_status(experiment_id: int, status: ExperimentStatus):
    experiments[experiment_id].status = status
    redis_connection.publish(
        'experiment_status',
        msgpack.packb({
            'experimentId': experiment_id,
            'status': status
        }))


def start_data_handling_for_experiment(exp: experiment.Experiment):
    device_manager = DeviceManager()
    commands_to_call = {}
    properties_to_call = {}
    for device_booking in exp.deviceBookings:
        device_uuid = device_booking.device
        features = device_manager.get_features_for_data_handler(device_uuid)
        for feature in features:
            for command in feature.commands:
                if command.active:
                    if command.meta:
                        interval_to_use = command.polling_interval_meta
                    else:
                        interval_to_use = command.polling_interval_non_meta
                    if (interval_to_use, device_booking.end) in commands_to_call.keys():
                        if device_uuid in commands_to_call[(interval_to_use,
                                                            device_booking.end)].keys():
                            commands_to_call[(interval_to_use,
                                              device_booking.end)][device_uuid].append((command, feature))
                        else:
                            commands_to_call[(interval_to_use,
                                              device_booking.end)][device_uuid] = [(command, feature)]
                    else:
                        commands_to_call[(interval_to_use,
                                          device_booking.end)] = {device_uuid: [(command, feature)]}
            for property in feature.properties:
                if property.active:
                    if property.meta:
                        interval_to_use = property.polling_interval_meta
                    else:
                        interval_to_use = property.polling_interval_non_meta
                    if (interval_to_use, device_booking.end) in properties_to_call.keys():
                        if device_uuid in properties_to_call[(interval_to_use,
                                                              device_booking.end)].keys():
                            properties_to_call[(interval_to_use,
                                                device_booking.end)][device_uuid].append((property, feature))
                        else:
                            properties_to_call[(interval_to_use,
                                                device_booking.end)][device_uuid] = [(property, feature)]
                    else:
                        properties_to_call[(interval_to_use,
                                            device_booking.end)] = {device_uuid: [(property, feature)]}
    jobs = data_handler.create_jobs(commands_to_call, properties_to_call)
    if exp.id in experiment_id_to_data_handler_jobs:
        experiment_id_to_data_handler_jobs[exp.id] = experiment_id_to_data_handler_jobs[exp.id] + jobs
    else:
        experiment_id_to_data_handler_jobs[exp.id] = jobs


def print_container_output(container):
    # container_output = container.attach(logs=False, stream=True)
    container_output = container.logs(follow=True, timestamps=True, stream=True, stdout=True, stderr=True)
    print('Output thread started!')
    with open("myContainerLog", "w") as file:
        for line in container_output:
            print(line.decode())
            file.write(line.decode())


def wait_until_container_stops(container, experiment_id: int,
                               status_queue: queue.SimpleQueue):
    status = container.wait()
    # print(container.logs())
    print(f'container stopped with StatusCode {status["StatusCode"]}')
    if status['StatusCode'] == 0:
        status_queue.put(
            ProcessStatusEvent(experiment_id,
                               ProcessStatusEventType.FINISHED_SUCCESSFUL))
    else:
        status_queue.put(
            ProcessStatusEvent(experiment_id, ProcessStatusEventType.ERROR))
    container.remove()


def start_experiment(experiment_id: int, status_queue: queue.SimpleQueue):
    exp = experiment.get_experiment(experiment_id)
    script = get_user_script(exp.scriptID)
    devices = [
        asdict(get_device_info(booking.device)) for booking in exp.deviceBookings
    ]
    start_data_handling_for_experiment(exp)
    client = docker.from_env()
    container = docker_helper.create_script_container(client, exp.name,
                                                      script.data,
                                                      f'devices={devices}')
    print(f'Created docker container for experiment {experiment_id}: \"{container.name}\"')

    output_thread = Thread(target=print_container_output, args=(container, ), daemon=True)

    wait_thread = Thread(target=wait_until_container_stops,
                         args=(container, experiment_id, status_queue))
    # Starting threads
    container.start()
    output_thread.start()
    wait_thread.start()

    status_queue.put(
        ProcessStatusEvent(experiment_id, ProcessStatusEventType.STARTED,
                           container.id))
    return


def handle_process_status_events(event: ProcessStatusEvent):
    if event.event_type == ProcessStatusEventType.STARTED:
        experiments[event.experiment_id].container_id = event.message
        change_experiment_status(event.experiment_id, ExperimentStatus.RUNNING)
        print(f'{experiments[event.experiment_id].name} started')
    elif event.event_type == ProcessStatusEventType.FINISHED_SUCCESSFUL:
        change_experiment_status(event.experiment_id,
                                 ExperimentStatus.FINISHED_SUCCESSFUL)
        print(f'{experiments[event.experiment_id].name} finished successful')
    elif event.event_type == ProcessStatusEventType.ERROR:
        change_experiment_status(event.experiment_id,
                                 ExperimentStatus.FINISHED_ERROR)
        print(f'{experiments[event.experiment_id].name} Error')


def event_listener(event):
    event_queue.put(event)


def handle_scheduling_events(event):
    if event.code == events.EVENT_JOB_SUBMITTED:
        if event.job_id in job_to_experiment:
            experiment_id = job_to_experiment[event.job_id]
            experiment_entry = experiments[experiment_id]
            change_experiment_status(experiment_id, ExperimentStatus.SUBMITED_FOR_EXECUTION)
            print(f'{experiment_entry.name} submitted')
    elif event.code == events.EVENT_JOB_REMOVED:
        if event.job_id in job_to_experiment:
            experiment_entry = experiments[job_to_experiment[event.job_id]]
            print(f'{experiment_entry.name} removed')
    elif event.code == events.EVENT_JOB_ERROR:
        if event.job_id in job_to_experiment:
            experiment_id = job_to_experiment[event.job_id]
            experiment_entry = experiments[experiment_id]
            change_experiment_status(experiment_id,
                                     ExperimentStatus.FINISHED_ERROR)
            print('scheduling error')
    elif event.code == events.EVENT_JOB_MISSED:
        if event.job_id in job_to_experiment:
            experiment_id = job_to_experiment[event.job_id]
            experiment_entry = experiments[experiment_id]
            change_experiment_status(experiment_id,
                                     ExperimentStatus.FINISHED_ERROR)
            print('experiment missed')


def schedule_future_experiments_from_database():
    for exp in experiment.get_scheduling_info():
        schedule_experiment(exp)


def schedule_experiment(exp: experiment.SchedulingInfo):
    if (exp.id not in experiments) or (
            experiments[exp.id].status == ExperimentStatus.FINISHED_ERROR or
            experiments[exp.id].status == ExperimentStatus.FINISHED_SUCCESSFUL
            or experiments[exp.id].status
            == ExperimentStatus.FINISHED_MANUALLY):
        job = scheduler.add_job(start_experiment,
                                'date',
                                args=[exp.id, process_status_queue],
                                name=f'experiment:{exp.name}',
                                run_date=datetime.fromtimestamp(exp.start))
        experiments[exp.id] = ExperimentState(
            exp.id, exp.name, job.id, '0', exp.start, exp.end,
            ExperimentStatus.WAITING_FOR_EXECUTION)
        job_to_experiment[job.id] = exp.id
        change_experiment_status(exp.id,
                                 ExperimentStatus.WAITING_FOR_EXECUTION)


def schedule_experiment_now(exp: experiment.SchedulingInfo):
    if (exp.id in experiments) and (
            experiments[exp.id].status != ExperimentStatus.FINISHED_ERROR or
            experiments[exp.id].status != ExperimentStatus.FINISHED_SUCCESSFUL
            or
            experiments[exp.id].status != ExperimentStatus.FINISHED_MANUALLY):
        stop_experiment(exp.id)

    job = scheduler.add_job(start_experiment,
                            args=[exp.id, process_status_queue],
                            name=f'experiment:{exp.name}')
    experiments[exp.id] = ExperimentState(
        exp.id, exp.name, job.id, '0', exp.start, exp.end,
        ExperimentStatus.WAITING_FOR_EXECUTION)
    job_to_experiment[job.id] = exp.id
    change_experiment_status(exp.id, ExperimentStatus.WAITING_FOR_EXECUTION)


def stop_experiment(experiment_id):
    # Stop data handling jobs for the experiment
    if experiment_id in experiment_id_to_data_handler_jobs:
        for job in experiment_id_to_data_handler_jobs[experiment_id]:
            job.remove()
        del experiment_id_to_data_handler_jobs[experiment_id]
    if experiment_id in experiments:
        experiment_entry = experiments[experiment_id]
        if experiment_entry.status == ExperimentStatus.WAITING_FOR_EXECUTION:
            scheduler.remove_job(experiment_entry.job_id)
            change_experiment_status(experiment_id,
                                     ExperimentStatus.FINISHED_MANUALLY)

        elif (experiment_entry.status ==
              ExperimentStatus.SUBMITED_FOR_EXECUTION) or (
                  experiment_entry.status == ExperimentStatus.RUNNING):
            try:
                client = docker.from_env()
                print(experiment_entry.container_id)
                container = client.containers.get(
                    experiment_entry.container_id)
                container.stop(timeout=1)
                change_experiment_status(experiment_id,
                                         ExperimentStatus.FINISHED_MANUALLY)
            except Exception:
                print("could not stop container")


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
