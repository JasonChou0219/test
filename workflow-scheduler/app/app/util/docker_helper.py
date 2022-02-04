import logging

import docker
import requests
from docker.models.containers import Container
from pydantic import Json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_node_red_executor_container(job_flow: Json):
    container = __start_node_red_executor_container()
    # time.sleep(5)
    __push_workflow_to_node_red_container(job_flow, container)
    return container


def __start_node_red_executor_container() -> Container:
    client = docker.from_env()
    container = client.containers.run('zechlin/node-red-executor', detach=True, network='sila2_manager_default')
    logger.info(f'Container {container.attrs["Name"]} created')
    # r = requests.get("http://workflow-designer:1880/flow-manager/flow-files/flow/Flow 1")
    # id = r.json()[0]['id']
    # r = requests.get(f'http://workflow-designer:1880/flow/{id}')
    # flow = r.json()
    return container


def __push_workflow_to_node_red_container(flow, container: Container):
    container.reload()
    ip = container.attrs['NetworkSettings']['Networks']['sila2_manager_default']['IPAddress']
    # Localhost only for non-docker testing
    # ip = "localhost"
    server_started_string = "Started flows"
    for line in container.logs(stream=True):
        if server_started_string in line.decode():
            break
    try:
        # change port to 1880 when running in docker
        s = requests.post(f'http://{ip}:1880/flow-manager/flow-files/flow/NewFlow', json=flow)
        logger.debug(s.text)
        s = requests.post(f'http://{ip}:1880/flow-manager/states', json={"action": "reloadOnly"})
        logger.debug(s.text)
    except Exception as e:
        logger.error(e)
        container.remove(force=True)
