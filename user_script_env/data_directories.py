import appdirs
import tempfile
from os import path, makedirs
from uuid import UUID

TEMP_DIRECTORY = path.join(tempfile.gettempdir(), 'device-manager')

def create_directories():
    makedirs(TEMP_DIRECTORY, exist_ok=True)
