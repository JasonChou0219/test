from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from source.device_manager.database import get_database_connection
import psycopg2


@dataclass
class BookingInfo:
    id: int
    name: str
    start: int
    end: int
    user: int
    device: UUID
    experiment: Optional[int] = None


@dataclass
class BookingInfoWithNames:
    id: int
    name: str
    start: int
    end: int
    user: int
    userName: str
    device: UUID
    deviceName: str
    experiment: Optional[int] = None
    experimentName: Optional[str] = None


def get_device_bookings_for_experiment_inside_transaction(
        conn, experiment: int) -> List[BookingInfoWithNames]:
    with conn.cursor() as cursor:
        cursor.execute(
            """
           select bookings.id,bookings.name,bookings.startTime,
           bookings.endTime,bookings.userID,users.name,bookings.device,devices.name,
           bookings.experiment,experiments.name from bookings 
           join experiments
           on bookings.experiment=experiments.id
           join users
           on bookings.userID=users.id
           join devices 
           on bookings.device=devices.uuid
           where bookings.experiment=%s 
           """, [experiment])
        return [
            BookingInfoWithNames(row[0], row[1], row[2], row[3], row[4],
                                 row[5], row[6], row[7], row[8], row[9])
            for row in cursor
        ]


def get_booking_entry(id: int) -> BookingInfo:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                'select id,name,startTime,endTime,userID,device,experiment from bookings where id=%s',
                [id])
            result = cursor.fetchone()
            return BookingInfo(result[0], result[1], result[2], result[3],
                               result[4], result[5], result[6])


def get_device_booking_info(device: UUID, start: int,
                            end: int) -> List[BookingInfo]:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f'select id,name,startTime,endTime,userID,device,experiment from bookings where device=%s' \
                f'and ((startTime>={start} and endTime<={end}) '\
                f'or ({start}>=startTime and {end}<=endTime) '\
                f'or (startTime<={start} and endTime>={start}) '\
                f'or (startTime<={end} and endTime>={end}))',
                [str(device)])
            return [
                BookingInfo(row[0], row[1], row[2], row[3], row[4], row[5],
                            row[6]) for row in cursor
            ]


def get_device_booking_info_with_names(device: UUID, start: int,
                                       end: int) -> List[BookingInfoWithNames]:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f'select bookings.id,bookings.name,bookings.startTime, '\
                f'bookings.endTime,bookings.userID,users.name,bookings.device,devices.name, ' \
                f'bookings.experiment,experiments.name '\
                f'from bookings '\
                f'left join experiments on bookings.experiment=experiments.id '\
                f'join users on bookings.device=devices.uuid '\
                f'join devices on bookings.userID=users.id '\
                f'where deviceID=%s ' \
                f'and ((bookings.startTime>={start} and bookings.endTime<={end}) '\
                f'or ({start}>=bookings.startTime and {end}<=bookings.endTime) '\
                f'or (bookings.startTime<={start} and bookings.endTime>={start}) '\
                f'or (bookings.startTime<={end} and bookings.endTime>={end}))',
                [str(device)])
            return [
                BookingInfoWithNames(row[0], row[1], row[2], row[3], row[4],
                                     row[5], row[6], row[7], row[8], row[9])
                for row in cursor
            ]


def get_booking_info(start: int, end: int) -> List[BookingInfo]:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'select id,name,start,end,user,device,experiment from bookings '\
                f'where (start>={start} and end<={end})'\
                f'or ({start}>=start and {end}<=end) '\
                f'or (start<={start} and end>={start}) '\
                f'or (start<={end} and end>={end})')
            return [
                BookingInfo(row[0], row[1], row[2], row[3], row[4], row[5],
                            row[6]) for row in cursor
            ]


def get_booking_info_with_names(start: int,
                                end: int) -> List[BookingInfoWithNames]:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f'select bookings.id,bookings.name,bookings.startTime, '\
                f'bookings.endTime,bookings.userID,users.name,bookings.device,devices.name,bookings.experiment,experiments.name '\
                f'from bookings '\
                f'left join experiments on bookings.experiment=experiments.id '\
                f'join users on bookings.userID=users.id '\
                f'join devices on bookings.device=devices.uuid '\
                f'where ((bookings.startTime>={start} and bookings.endTime<={end})'\
                f'or ({start}>=bookings.startTime and {end}<=bookings.endTime) '\
                f'or (bookings.startTime<={start} and bookings.endTime>={start}) '\
                f'or (bookings.startTime<={end} and bookings.endTime>={end}))')
            return [
                BookingInfoWithNames(row[0], row[1], row[2], row[3], row[4],
                                     row[5], row[6], row[7], row[8], row[9])
                for row in cursor
            ]


def is_now_free_inside_transaction(conn, device: UUID) -> bool:
    now = int(datetime.now().timestamp())
    with conn.cursor() as cursor:
        cursor.execute(f'select count(id) from bookings '\
            f'where device =%s and startTime<={now} and {now}<=endTime',[str(device)])
        result = cursor.fetchone()
        if result is None:
            return True
        return result[0] == 0


def is_now_free(device: UUID) -> bool:
    with get_database_connection() as conn:
        return is_now_free_inside_transaction(conn, device)


def is_time_range_free_inside_transaction(conn, device: UUID, start: int,
                                          end: int) -> bool:
    with conn.cursor() as cursor:
        cursor.execute(f'select count(id) from bookings '\
            f'where device=%s and ((startTime>={start} and endTime<={end}) '\
            f'or ({start}>=startTime and {end}<=endTime) '\
            f'or (startTime<={start} and endTime>={start}) '\
            f'or (startTime<={end} and endTime>={end}))',[str(device)])
        result = cursor.fetchone()
        if result is None:
            return True
        return result[0] == 0


def is_time_range_free(device: UUID, start: int, end: int) -> bool:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'select count(id) from bookings '\
                f'where device=%s and ((startTime>={start} and endTime<={end}) '\
                f'or ({start}>=startTime and {end}<=endTime) '\
                f'or (startTime<={start} and endTime>={start}) '\
                f'or (startTime<={end} and endTime>={end}))',[str(device)])
            result = cursor.fetchone()
            if result is None:
                return True
            return result[0] == 0


def book_inside_transaction(conn, info: BookingInfo) -> int:
    if is_time_range_free_inside_transaction(conn, info.device, info.start,
                                             info.end):
        with conn.cursor() as cursor:
            cursor.execute(
                'insert into bookings values (default,%s,%s,%s,%s,%s,%s) returning id',
                [
                    info.name, info.start, info.end, info.user,
                    str(info.device), info.experiment
                ])
            booking_id = cursor.fetchone()[0]
            return booking_id
    else:
        return -1


def book(info: BookingInfo) -> int:
    with get_database_connection() as conn:
        return book_inside_transaction(conn, info)


def id_is_valid(id: int) -> bool:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('select * from bookings where id=%s', [id])
            return len(cursor.fetchall()) > 0


def delete_booking_entry(id: int):
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('delete from bookings where id=%s', [id])
