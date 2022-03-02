import os
import logging
import uuid

import tarfile
import docker
import requests
from docker.models.containers import Container
from docker.types import LogConfig, DriverConfig
from pydantic import Json

from app.util.data_directories import TEMP_DIRECTORY

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


def _delete_file(file_name: str):
    if os.path.exists(file_name):
        os.remove(file_name)


def _set_workflow_filename(tarinfo):
    tarinfo.name = 'workflow.py'
    return tarinfo


def _set_services_filename(tarinfo):
    tarinfo.name = 'services.py'
    return tarinfo


def _create_temporary_tar(workflow_data: str, services_data: str):
    os.makedirs(f'{TEMP_DIRECTORY}/container', exist_ok=True)
    title = str(uuid.uuid4())
    workflow_file = f'{TEMP_DIRECTORY}/container/{title}_workflow.py'
    services_file = f'{TEMP_DIRECTORY}/container/{title}_services.py'
    tar_file = f'{TEMP_DIRECTORY}/container/{title}.tar'
    _delete_file(workflow_file)
    _delete_file(services_file)
    with open(workflow_file, mode='x') as f:
        f.write(workflow_data)
    with open(services_file, mode='x') as f:
        f.write(services_data)
    _delete_file(tar_file)
    with tarfile.open(tar_file, mode='x') as tar:
        tar.add(workflow_file, filter=_set_workflow_filename)
        tar.add(services_file, filter=_set_services_filename)
    _delete_file(workflow_file)
    _delete_file(services_file)
    return tar_file

def create_python_workflow_image(docker_client, image_name: str):
    image, logs = docker_client.images.build(path='app/workflow-executor-python/', tag=image_name)
    return image

def create_python_workflow_container(docker_client, image_name: str, container_name: str, workflow_data: str, services_data: str):
    dc = DriverConfig(name='local', options={
        'max-size': '10m'
    })
    # publish_all_ports
    extra_hosts = {'host.docker.internal': 'host-gateway'}
    container = docker_client.containers.create(
        image_name,
        'python main.py',
        name=container_name,
        # detach=False,
        log_config=dc,
        # publish_all_ports=True,
        network_mode='host',
        extra_hosts=extra_hosts,
    )
    # devices_data = re.sub(r"'localhost'", "'host.docker.internal'", devices_data)
    # devices_data = re.sub(r"'127.0.0.1'", "'host.docker.internal'", devices_data)
    # devices_data = re.sub(r"'0.0.0.0'", "'host.docker.internal'", devices_data)

    tar = _create_temporary_tar(workflow_data, services_data)
    with open(tar, "rb") as tar_file:
        buff = tar_file.read()
        container.put_archive('/usr/src/app', buff)
    _delete_file(tar)
    return container
