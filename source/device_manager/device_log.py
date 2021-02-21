from dataclasses import dataclass
from typing import List
from enum import IntEnum
import psycopg2
from datetime import datetime
from source.device_manager.database import get_database_connection, release_database_connection
import logging


class LogLevel(IntEnum):
    INFO = 0,
    WARNING = 1
    CRITICAL = 2,
    ERROR = 3


@dataclass
class LogEntry:
    type: LogLevel
    device: str
    time: int
    message: str


def now() -> int:
    return int(datetime.now().timestamp())


def log(type: LogLevel, device: str, message: str, time: int = now()):
    conn = get_database_connection()
    conn.cursor().execute(f'insert into log values (default,%s,%s,%s,%s)',
                          [type, device, time, message])
    conn.commit()
    release_database_connection(conn)


def info(device: str, message: str, time: int = now()):
    log(LogLevel.INFO, device, message, time)


def warning(device: str, message: str, time: int = now()):
    log(LogLevel.WARNING, device, message, time)


def critical(device: str, message: str, time: int = now()):
    log(LogLevel.CRITICAL, device, message, time)


def error(device: str, message: str, time: int = now()):
    log(LogLevel.ERROR, device, message, time)


class DeviceManagerLogHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record: logging.LogRecord):
        message = self.format(record)
        time = int(record.created)
        if record.levelno == logging.INFO:
            info('Device Manager', message, time)
        elif record.levelno == logging.WARNING:
            warning('Device Manager', message, time)
        elif record.levelno == logging.CRITICAL:
            critical('Device Manager', message, time)
        elif record.levelno == logging.ERROR:
            error('Device Manager', message, time)
