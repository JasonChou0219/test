#!/usr/bin/env python3
import docker
import tarfile
import uuid
from threading import Thread
import os
import sys
import time
from source.device_manager.data_directories import TEMP_DIRECTORY


def _delete_file(file_name: str):
    if os.path.exists(file_name):
        os.remove(file_name)


def _set_name(tarinfo):
    tarinfo.name = 'script.py'
    return tarinfo


def _create_temporary_tar(data: str):
    os.makedirs(f'{TEMP_DIRECTORY}/container', exist_ok=True)
    name = str(uuid.uuid4())
    script_file = f'{TEMP_DIRECTORY}/container/{name}.py'
    tar_file = f'{TEMP_DIRECTORY}/container/{name}.tar'
    _delete_file(script_file)
    with open(script_file, mode='x') as script:
        script.write(data)
    _delete_file(tar_file)
    with tarfile.open(tar_file, mode='x') as tar:
        tar.add(script_file, filter=_set_name)
    _delete_file(script_file)
    return tar_file


def create_script_container(docker_client, container_name: str, data: str):
    container = docker_client.containers.create(
        'user_script',
        'python script.py',
        name=container_name,
    )
    tar = _create_temporary_tar(data)
    with open(tar, "rb") as tar_file:
        buff = tar_file.read()
        container.put_archive('/usr/src/app', buff)
    _delete_file(tar)
    return container
