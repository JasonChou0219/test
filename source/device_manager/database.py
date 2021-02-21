import psycopg2
from psycopg2 import pool
import aioredis
from os import path
import configparser

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
    if storage.get('pool') is None:
        if storage.get('dbconf') is None:
            config = configparser.ConfigParser()
            config.read(f'{DATA_DIRECTORY}/device-manager.conf')
            storage['dbconf'] = config['Database']
        dbconf = storage['dbconf']
        storage['pool'] = psycopg2.pool.SimpleConnectionPool(1, 
                                           20,
                                           host=dbconf['host'],
                                           port=dbconf['port'],
                                           user=dbconf['user'],
                                           password=dbconf['password'])
    return storage['pool'].getconn()

def release_database_connection(connection):
    pool=storage.get('pool')
    if pool is not None:
        pool.putconn(connection)
