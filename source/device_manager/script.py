from dataclasses import dataclass
from typing import List
from source.device_manager.database import get_database_connection


@dataclass
class ScriptInfo:
    id: int
    name: str
    fileName: str
    user: int


@dataclass
class Script:
    id: int
    name: str
    fileName: str
    user: int
    data: str


def get_user_scripts(user: int) -> List[Script]:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                select scripts.id, scripts.name,scripts.fileName,scripts.userID,scripts.data
                from scripts where userID=%s
                """, [user])
            return [
                Script(row[0], row[1], row[2], row[3], row[4])
                for row in cursor
            ]


def get_user_scripts_info(user: int) -> List[ScriptInfo]:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                select scripts.id, scripts.name,scripts.fileName,scripts.userID 
                from scripts where userID=%s
                """, [user])
            return [
                ScriptInfo(row[0], row[1], row[2], row[3]) for row in cursor
            ]


def get_user_script(script_id: int) -> Script:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                select scripts.id, scripts.name,scripts.fileName,scripts.userID,scripts.data
                from scripts where id=%s
                """, [script_id])
            result = cursor.fetchone()
            return Script(result[0], result[1], result[2], result[3],
                          result[4])


def get_user_script_info(script_id: int) -> ScriptInfo:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                select scripts.id, scripts.name,scripts.fileName,scripts.userID 
                from scripts where id=%s
                """, [script_id])
            result = cursor.fetchone()
            return ScriptInfo(result[0], result[1], result[2], result[3])


def create_user_script(name: str, file_name: str, user: int, data: str) -> int:
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                'insert into scripts values (default,%s,%s,%s,%s) returning id',
                [name, file_name, user, data])
            return cursor.fetchone()[0]


def set_user_script_info(script_id: int, name: str, file_name: str,
                         user_id: int):
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                'update scripts set name=%s, fileName=%s, userID=%s where id=%s',
                [name, file_name, user_id, script_id])


def set_user_script(script_id: int, name: str, file_name: str, user_id: int,
                    data: str):
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                'update scripts set name=%s, fileName=%s, userID=%s, data=%s where id=%s',
                [name, file_name, user_id, data, script_id])


def delete_user_script(script_id: int):
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('delete from scripts where id=%s', [script_id])
