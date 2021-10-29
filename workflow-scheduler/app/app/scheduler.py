import queue
import time
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler import events

from util.database import get_scheduling_info

event_queue = queue.SimpleQueue()
scheduler = BackgroundScheduler()

experiments = {}
job_to_experiment = {}


def event_listener(event):
    event_queue.put(event)


# def schedule_future_jobs_from_database():
#     for job in experiment.get_scheduling_info():
#         schedule_experiment(job)
#
#
# def schedule_experiment(job: experiment.SchedulingInfo):
#     if (job.id not in experiments) or (
#             experiments[job.id].status == ExperimentStatus.FINISHED_ERROR or
#             experiments[job.id].status == ExperimentStatus.FINISHED_SUCCESSFUL
#             or experiments[job.id].status
#             == ExperimentStatus.FINISHED_MANUALLY):
#         job = scheduler.add_job(start_experiment,
#                                 'date',
#                                 args=[job.id, process_status_queue],
#                                 name=f'experiment:{job.name}',
#                                 run_date=datetime.fromtimestamp(job.start))
#         experiments[job.id] = ExperimentState(
#             job.id, job.name, job.id, '0', job.start, job.end,
#             ExperimentStatus.WAITING_FOR_EXECUTION, deque(['Starting experiment..\n', 'Connection established.\n'],
#                                                           maxlen=EXPERIMENT_LOG_BUFFER_LENGTH))
#         job_to_experiment[job.id] = job.id
#         change_experiment_status(job.id,
#                                  ExperimentStatus.WAITING_FOR_EXECUTION)


def main():
    print(get_scheduling_info())
    # scheduler.add_listener(event_listener, events.EVENT_ALL)
    # scheduler.start()
    # schedule_future_experiments_from_database()
    # t = time.time()
    # while True:
    #     try:
    #         handle_scheduling_events(event_queue.get_nowait())
    #     except queue.Empty:
    #         pass
    #
    #     try:
    #         handle_process_status_events(process_status_queue.get_nowait())
    #     except queue.Empty:
    #         pass
    #
    #     receive_and_execute_commands()
    #     t2 = time.time()
    #     if t2 - t >= 5:
    #         t = t2
    #         schedule_future_experiments_from_database()
    #
    # scheduler.shutdown()


if __name__ == '__main__':
    main()
