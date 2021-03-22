import psycopg2
from psycopg2 import pool
import aioredis
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
        storage['pool'] = psycopg2.pool.SimpleConnectionPool(minconn=1,
                                                             maxconn=2000,
                                                             host=dbconf['host'],
                                                             port=dbconf['port'],
                                                             user=dbconf['user'],
                                                             password=dbconf['password'])
    return storage['pool'].getconn()


def release_database_connection(connection):
    storage = get_storage()
    pool = storage.get('pool')
    print('Pool is:', pool)
    print('Pool used connections:', pool._used)

    if pool is not None:
        # Use close=False (default) to increase speed. However, this option will not close but only suspend the
        # connection, indirectly restricting the number of total connections, i.e. devices and users to access.
        # putconn(conn, key=None, close=False)
        pool.putconn(connection, close=True)
