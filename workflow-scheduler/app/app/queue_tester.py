import json
import os
from datetime import datetime
from queue import Queue
from threading import Thread

import docker
import keyboard as keyboard
from docker.models.containers import Container

log_dict = {}


def get_queue_item(q: Queue):
    i = q.get()
    q.task_done()
    return i


def get_container_logs(cnt: Container):
    logs = log_dict[cnt.id].queue
    return logs


def store_container_logs(container: Container, job_id, workflow_id):
    lgs = container.logs(follow=True, timestamps=True, stream=True, stdout=True, stderr=True)
    for line in lgs:
        log_dict[job_id][workflow_id][1].put(line.decode())
        # print(line.decode())


def prune_logs(max_queue_size: int, prune_amount: int):
    for key in log_dict:
        if log_dict[key][2].qsize() > max_queue_size:
            for i in range(prune_amount):
                log_dict[key][2].get()


def start_container_log_storage(container: Container, job_id, workflow_id, queue_size: int):
    if not isinstance(log_dict[job_id], dict): log_dict[job_id] = {}
    log_dict[job_id][workflow_id] = (container.id, Queue(queue_size),
                                     container.logs(follow=True, timestamps=True, stream=True, stdout=True,
                                                    stderr=True))
    log_thread = Thread(target=store_container_logs, args=(container, job_id, workflow_id), daemon=True)
    log_thread.start()


def add_job_to_log_dict(job_id):
    log_dict.setdefault(job_id, {})


def main():
    client = docker.from_env()
    # log_dict.setdefault(1, )
    container = client.containers.create("nodered/node-red")
    container.start()
    start_container_log_storage(container, 1, 1, 20)
    # print(log_dict[container.id])
    try:
        while True:
            if keyboard.read_key() == "p":
                log_path = os.path.join(os.path.abspath("C:\\Users\\rzech\\Desktop"), 'container',
                                        f'{datetime.now().strftime("%d_%m_%Y-%H_%M_%S")}_.log')
                # print_out = json.dumps(get_container_logs(container))
                # print_out = get_container_logs(container)
                with open(log_path, "w") as file:
                    for line in get_container_logs(container):
                        file.write(line)

                # lgs = container.logs(follow=True, timestamps=True, stream=True, stdout=True, stderr=True)
                # for line in lgs:
                #     print(line.decode())

                # print(print_out)
    except KeyboardInterrupt:
        pass
    finally:
        container.remove(force=True)


def create_dict_if_not_exists(d: dict):
    pass


def tester():
    # q = log_dict['test']['test2'] = (1, Queue())

    dicta = {}
    # dicta['a'] = {}
    # dicta['a']['b'] = 2

    # while True:
    #     prune_logs(5, 5)
    #     q[1].put(1)
    #     print(q[2].qsize())
    i = 0
    for i in range(3):
        dicta.setdefault(f'job_id {i}', {})
        for j in range(2):
            dicta[f'job_id {i}'].setdefault(f'wf_id {j}', {})
        # print(dicta)

    print(dicta)


if __name__ == '__main__':
    # main()
    tester()
