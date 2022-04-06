import json
import os
import random
from datetime import datetime
from queue import Queue
from threading import Thread

import docker
import keyboard as keyboard
from docker.models.containers import Container
from util import docker_helper
import asyncio
import websockets


log_dict = {}
image_name = 'workflow_executor_python'
services = 'None'
workflow = "import logging\r\nimport time\r\nfrom datetime import datetime\r\n\r\ndef run():\r\n    while True:\r\n   " \
           "     print(datetime.now(), flush=True)\r\n        time.sleep(2)\r\n        # logger.debug(datetime.now(" \
           "))\r\n\r\n\r\n\r\n "



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
        log_dict[job_id][workflow_id]['log_buffer'].put(line.decode())
        # print(line.decode())


def prune_logs(max_queue_size: int, prune_amount: int):
    while True:
        for key in log_dict:
            for key2 in log_dict[key]:
                if log_dict[key][key2]['log_buffer'].qsize() > max_queue_size:
                    for i in range(prune_amount):
                        log_dict[key][key2]['log_buffer'].get()


def start_container_log_storage(container: Container, job_id: str, workflow_id: str, queue_size: int):
    if not isinstance(log_dict[job_id], dict): log_dict[job_id] = {}
    log_dict[job_id].setdefault(workflow_id, {'container_id': container.id,
                                                    'log_buffer': Queue(queue_size),
                                                    'log_stream': container.logs(follow=True, timestamps=True,
                                                                                 stream=True, stdout=True,
                                                                                 stderr=True)
                                                    })
    log_thread = Thread(target=store_container_logs, args=(container, job_id, workflow_id), daemon=True)
    log_thread.start()


def add_job_to_log_dict(job_id):
    log_dict.setdefault(job_id, {})


def main():
    docker_client = docker.from_env()
    # log_dict.setdefault(1, )
    log_dict.setdefault(1, {})
    containers = []
    for container_id in range(1):
        container_name = f'Test_{container_id}_{random.randint(0,1000)}'
        container = docker_helper.create_python_workflow_container(
            docker_client,
            image_name,
            container_name,
            workflow,
            f'services={services}'
        )
        container.start()
        start_container_log_storage(container, 1, container_id, 20)
        containers.append(container)
    # print(log_dict[container.id])
    start_server = websockets.serve(websocket_server, 'localhost', 8765)

    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        prune_thread = Thread(target=prune_logs, args=(17, 3), daemon=True)
        prune_thread.start()
        asyncio.get_event_loop().run_forever()
    # try:
    #     while True:
    #         if keyboard.read_key() == "p":
    #             log_path = os.path.join(os.path.abspath("C:\\Users\\rzech\\Desktop"), 'container',
    #                                     f'{datetime.now().strftime("%d_%m_%Y-%H_%M_%S")}_.log')
    #             # print_out = json.dumps(get_container_logs(container))
    #             # print_out = get_container_logs(container)
    #             with open(log_path, "w") as file:
    #                 for line in get_container_logs(container):
    #                     file.write(line)
    #
    #             # lgs = container.logs(follow=True, timestamps=True, stream=True, stdout=True, stderr=True)
    #             # for line in lgs:
    #             #     print(line.decode())
    #
    #             # print(print_out)
    except KeyboardInterrupt:
        for cnt in containers:
            cnt.remove(force=True)
    # finally:
    #     container.remove(force=True)


def create_dict_if_not_exists(d: dict):
    pass


async def websocket_server(websocket, path):
    # id = await websocket.recv()

    lgs = list(log_dict[1][0]["log_buffer"].queue)

    for item in lgs:
        # print(type(item))
        await websocket.send(item)

    stream = log_dict[1][0]["log_stream"]
    for line in stream:
        # print(line.decode())
        await websocket.send(line.decode())


# def tester():
#     # q = log_dict['test']['test2'] = (1, Queue())
#
#     dicta = {}
#     # dicta['a'] = {}
#     # dicta['a']['b'] = 2
#
#     # while True:
#     #     prune_logs(5, 5)
#     #     q[1].put(1)
#     #     print(q[2].qsize())
#     i = 0
#     for i in range(3):
#         dicta.setdefault(f'job_id {i}', {})
#         for j in range(2):
#             dicta[f'job_id {i}'].setdefault(f'wf_id {j}', {})
#         # print(dicta)
#
#     print(dicta)


if __name__ == '__main__':
    main()
    # tester()
