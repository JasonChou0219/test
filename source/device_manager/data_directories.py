import appdirs
import tempfile
from os import path, makedirs,environ
from uuid import UUID


DATA_DIRECTORY='/etc/device-manager'
env = environ.get('DEVICE_MANAGER_ENV_PRODUCTION')

if env is None or env == '0':
    DATA_DIRECTORY = appdirs.user_data_dir('device-manager')

TEMP_DIRECTORY = path.join(tempfile.gettempdir(), 'device-manager')


def create_directories():
    makedirs(DATA_DIRECTORY, exist_ok=True)
    makedirs(TEMP_DIRECTORY, exist_ok=True)
