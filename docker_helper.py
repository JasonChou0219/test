#!/usr/bin/env python3
import tarfile
import uuid
import os
from source.device_manager.data_directories import TEMP_DIRECTORY
from docker.types import LogConfig, DriverConfig
import re


def _delete_file(file_name: str):
    if os.path.exists(file_name):
        os.remove(file_name)


def _set_script_filename(tarinfo):
    tarinfo.name = 'script.py'
    return tarinfo


def _set_devices_filename(tarinfo):
    tarinfo.name = 'devices.py'
    return tarinfo


def _create_temporary_tar(script_data: str, devices_data: str):
    os.makedirs(f'{TEMP_DIRECTORY}/container', exist_ok=True)
    name = str(uuid.uuid4())
    script_file = f'{TEMP_DIRECTORY}/container/{name}_script.py'
    devices_file = f'{TEMP_DIRECTORY}/container/{name}_devices.py'
    tar_file = f'{TEMP_DIRECTORY}/container/{name}.tar'
    _delete_file(script_file)
    _delete_file(devices_file)
    with open(script_file, mode='x') as f:
        f.write(script_data)
    with open(devices_file, mode='x') as f:
        f.write(devices_data)
    _delete_file(tar_file)
    with tarfile.open(tar_file, mode='x') as tar:
        tar.add(script_file, filter=_set_script_filename)
        tar.add(devices_file, filter=_set_devices_filename)
    _delete_file(script_file)
    _delete_file(devices_file)
    return tar_file


def create_script_container(docker_client, container_name: str, script_data: str, devices_data: str):
    dc = DriverConfig(name='local', options={
        'max-size': '10m'
    })
    lc = LogConfig(type='json-file', config={
        'max-size': '1m',
        'max-file': 3
    })
    # publish_all_ports
    container = docker_client.containers.create(
        'user_script',
        'python main.py',
        name=container_name,
        # detach=False,
        log_config=dc,
        # publish_all_ports=True,
        network_mode='host',
        # ports={'50003/tcp': 50003,
               #'50003/udp': 50003,
               #'8080/tcp': 8080,
               #'80/tcp': 80,
               #'9090/tcp': 9090,
               #'55001/tcp': 55001,
               # '5000/tcp': ('127.0.0.1', 5000),
        #       }
    )
    devices_data = re.sub(r"'localhost'", "'host.docker.internal'", devices_data)
    devices_data = re.sub(r"'127.0.0.1'", "'host.docker.internal'", devices_data)
    devices_data = re.sub(r"'0.0.0.0'", "'host.docker.internal'", devices_data)

    tar = _create_temporary_tar(script_data, devices_data)
    with open(tar, "rb") as tar_file:
        buff = tar_file.read()
        container.put_archive('/usr/src/app', buff)
    _delete_file(tar)
    return container

