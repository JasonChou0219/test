import psycopg2
import aioredis
from os import path

from .data_directories import DATA_DIRECTORY
from .thread_local_storage import get_storage


async def get_redis_pool():
    storage = get_storage()
    if storage.get('redis') is None:
        storage['redis'] = await aioredis.create_redis_pool('redis://localhost'
                                                            )
    return storage['redis']


def get_database_connection():
    storage = get_storage()
    if storage.get('conn') is None:
        #TODO read connection parameters from config file
        storage['conn'] = psycopg2.connect(host='localhost',
                                           port=5432,
                                           user='postgres',
                                           password='1234')
    return storage['conn']
