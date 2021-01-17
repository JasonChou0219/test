import psycopg2
import aioredis
from os import path

from .data_directories import DATA_DIRECTORY
from .thread_local_storage import get_storage
from .global_storage import get_global_storage


async def get_redis_pool():
    storage = get_storage()
    if storage.get('redis') is None:
        storage['redis'] = await aioredis.create_redis_pool('redis://localhost'
                                                            )
    return storage['redis']


def get_database_connection():
    storage = get_storage()
    if storage.get('conn') is None:
        config = get_global_storage().get('config')['Database']
        storage['conn'] = psycopg2.connect(host=config['host'],
                                           port=config['port'],
                                           user=config['user'],
                                           password=config['password'])
    return storage['conn']
