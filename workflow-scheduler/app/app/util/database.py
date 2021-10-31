import json
import threading
from datetime import datetime
from typing import List

import psycopg2
from psycopg2 import pool
import aioredis
import configparser
import logging

from app.schemas.job import Job

# from .data_directories import DATA_DIRECTORY
# from .thread_local_storage import get_storage

__storage = threading.local()


def get_scheduling_info() -> List[Job]:
    now = datetime.now()
    info = []
    conn = get_database_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                'select uuid, flow, flow_id, description, title, created_at, execute_at, owner_id '
                'from job '
                'where job.execute_at <= %s '
                'order by job.execute_at', [now])
            result = cursor.fetchall()
            info = [
                Job(uuid=row[0],
                    flow=json.dumps(row[1]),
                    flow_id=row[2],
                    description=row[3],
                    title=row[4],
                    created_at=row[5],
                    execute_at=row[6],
                    owner_id=row[7])
                for row in result
            ]
    release_database_connection(conn)
    return info


def get_storage():
    val = getattr(__storage, 'val', None)
    if val is None:
        __storage.val = {}
    return __storage.val


def get_database_connection():
    storage = get_storage()
    if storage.get('pool') is None:
        storage['pool'] = psycopg2.pool.ThreadedConnectionPool(minconn=1,
                                                               maxconn=2000,
                                                               host='localhost',
                                                               port='6432',
                                                               user='postgres',
                                                               password='DIB-central',
                                                               dbname='workflow-scheduler'
                                                               )
    logging.debug('Pool size is:', len(storage['pool']._used))
    for i in range(3):
        try:
            conn = storage['pool'].getconn()
            break
        except Exception as e:
            logging.exception('Pool size is:', len(storage['pool']._used))
            logging.exception(e)
            storage['pool'].closeall()
            continue

    return conn


def release_database_connection(connection):
    storage = get_storage()
    pool = storage.get('pool')
    logging.info(f'Pool is: {pool}')
    logging.info(f'Pool used connections: {pool._used}')

    if pool is not None:
        # Use close=False (default) to increase speed. However, this option will not close but only suspend the
        # connection, indirectly restricting the number of total connections, i.e. devices and users to access.
        # putconn(conn, key=None, close=False)
        pool.putconn(connection, close=True)
