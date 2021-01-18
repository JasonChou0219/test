#!/usr/bin/env python3
import secrets
import base64
import configparser
import os
from source.device_manager.data_directories import DATA_DIRECTORY

DIRECTORY = DATA_DIRECTORY
CONFIG_FILE = f'{DIRECTORY}/device-manager.conf'

config = configparser.ConfigParser()
config['Security'] = {
    'SecretKey': base64.b64encode(secrets.token_bytes(64)).decode()
}
config['Database'] = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': '1234'
}

os.makedirs(DIRECTORY, exist_ok=True)
with open(CONFIG_FILE, 'w') as configfile:
    config.write(configfile)
