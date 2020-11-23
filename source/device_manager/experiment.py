from dataclasses import dataclass
from typing import List
from datetime import datetime
from uuid import UUID
import msgpack
import redis
from source.device_manager.database import get_database_connection, get_redis_pool
from source.device_manager.scheduler import BookingInfo, BookingInfoWithNames, get_device_bookings_for_experiment_inside_transaction, book_inside_transaction


@dataclass
class SchedulingInfo:
    id: int
    name: str
    start: int
    end: int
    scriptID: int


@dataclass
class Experiment:
    id: int
    name: str
    start: int
    end: int
    user: str
    deviceBookings: List[BookingInfoWithNames]
    scriptID: int
    scriptName: int


def get_experiment_name(id: int) -> str:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('select name from experiments where id=%s', [id])
            return cursor.fetchone()


def get_experiment_user(id: int) -> int:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('select userID from experiments where id=%s', [id])
            return cursor.fetchone()


def get_experiment(id: int) -> Experiment:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('select experiments.id, experiments.name,experiments.startTime,'\
                           'experiments.endTime,users.name,experiments.script,scripts.name '\
                           'from experiments join scripts on experiments.script=scripts.id '\
                           'join users on experiments.userID=users.id '\
                           'where experiments.id=%s',[id])
            result = cursor.fetchone()
            experiment = Experiment(result[0], result[1], result[2], result[3],
                                    result[4], [], result[5], result[6])

            experiment.deviceBookings = get_device_bookings_for_experiment_inside_transaction(
                conn, experiment.id)
            return experiment


def get_all_experiments() -> List[Experiment]:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('select experiments.id, experiments.name,experiments.startTime,'\
                           'experiments.endTime,users.name,experiments.script,scripts.name '\
                           'from experiments join scripts on experiments.script=scripts.id '\
                           'join users on experiments.userID=users.id')
            experiments = [
                Experiment(row[0], row[1], row[2], row[3], row[4], [], row[5],
                           row[6]) for row in cursor
            ]

            for experiment in experiments:
                experiment.deviceBookings = get_device_bookings_for_experiment_inside_transaction(
                    conn, experiment.id)
            return experiments


def get_user_experiments(user: int) -> List[Experiment]:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('select experiments.id, experiments.name,experiments.startTime,'\
                           'experiments.endTime,experiments.userID,experiments.script,scripts.name '\
                           'from experiments join scripts on experiments.script=scripts.id where experiments.userID=%s',[user])
            experiments = [
                Experiment(row[0], row[1], row[2], row[3], row[4], [], row[5],
                           row[6]) for row in cursor
            ]

            for experiment in experiments:
                experiment.deviceBookings = get_device_bookings_for_experiment_inside_transaction(
                    conn, experiment.id)
            return experiments


def get_scheduling_info() -> List[SchedulingInfo]:
    now = int(datetime.timestamp(datetime.now()))
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('select id, name, startTime, endTime, script '
                           'from experiments '
                           'where experiments.startTime>=%s '
                           'order by experiments.startTime', [now])
            return [
                SchedulingInfo(row[0], row[1], row[2], row[3], row[4])
                for row in cursor
            ]


def create_experiment(name: str, start: int, end: int, user: int,
                      devices: List[UUID], script: int) -> int:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                'insert into experiments values (default,%s,%s,%s,%s,%s) returning id',
                [name, start, end, user, script])
            experiment_id = cursor.fetchone()[0]
            for device in devices:
                if book_inside_transaction(
                        conn,
                        BookingInfo(-1, name, start, end, user, device,
                                    experiment_id)) < 0:
                    conn.rollback()
                    return -1
            return experiment_id


def delete_experiment(experimentID: int):
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('delete from experiments where id=%s',
                           [experimentID])
            cursor.execute('delete from bookings where experiment=%s',
                           [experimentID])


async def _publish_command(command: str, params: list):
    pool = await get_redis_pool()
    with await pool as conn:
        await conn.publish(
            'scheduler', msgpack.packb({
                'command': command,
                'params': params
            }))


async def start_experiment(experimentID: int):
    await _publish_command('start', [experimentID])


async def stop_experiment(experimentID: int):
    await _publish_command('stop', [experimentID])


async def get_status(experimentID: int):
    await _publish_command('status', [experimentID])
