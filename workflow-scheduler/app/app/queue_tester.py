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


def store_container_logs(container):
    lgs = container.logs(follow=True, timestamps=True, stream=True, stdout=True, stderr=True)
    for line in lgs:
        log_dict[container.id].put(line.decode())
        # print(line.decode())


def prune_logs(max_queue_size: int, prune_amount: int):
    for key in log_dict:
        if log_dict[key][2].qsize() > max_queue_size:
            for i in range(prune_amount):
                log_dict[key][2].get()


def start_container_log_storage(container: Container, job_id, workflow_id, queue_size: int):
    log_dict[workflow_id] = (container.id, job_id, Queue(queue_size))
    log_thread = Thread(target=store_container_logs, args=(container,), daemon=True)
    log_thread.start()


def main():
    client = docker.from_env()
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

                # print(print_out)
    except KeyboardInterrupt:
        pass
    finally:
        container.remove(force=True)


def tester():
    q = log_dict['test'] = (1,1,Queue())
    while True:
        prune_logs(5, 5)
        q[2].put(1)
        print(q[2].qsize())


if __name__ == '__main__':
    # main()
    tester()

