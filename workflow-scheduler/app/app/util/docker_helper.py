import logging
import requests
import time

import docker
from docker.models.containers import Container
from pydantic import Json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_flow_container(job_flow: Json):
    container = __start_container()
    __push_workflow_to_container(job_flow, container)


def __start_container() -> Container:
    client = docker.from_env()
    container = client.containers.run('zechlin/node-red-executor', detach=True, network='sila2_manager_default'
                                           , ports={1880:2880})
    # r = requests.get("http://workflow-designer:1880/flow-manager/flow-files/flow/Flow 1")
    # id = r.json()[0]['id']
    # r = requests.get(f'http://workflow-designer:1880/flow/{id}')
    # flow = r.json()
    return container


def __push_workflow_to_container(flow, container: Container):
    container.reload()
    ip = container.attrs['NetworkSettings']['Networks']['sila2_manager_default']['IPAddress']
    server_started_string = "Started flows"
    for line in container.logs(stream=True):
        if server_started_string in line.decode():
            break
    try:
        s = requests.post(f'http://{ip}:1880/flow', json=flow)
    except Exception as e:
        print(e)
        container.remove(force=True)

