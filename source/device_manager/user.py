import hashlib
import os
import base64
from dataclasses import dataclass
from source.device_manager.database import get_database_connection
from typing import List
import logging
import sys


class UserError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class UserExistsError(UserError):
    def __init__(self, username):
        super().__init__(
            f"can't create user {username}. The username exists already")
        self.username = username


@dataclass
class User:
    id: int
    name: str
    fullName: str
    passwordHash: str
    role: str


def get_user(id: int) -> User:
    with get_database_connection() as conn:
        with conn.cursor() as c:
            c.execute(
                'select id,name,fullName,passwordHash,role from users where id=%s',
                [id])
            result = c.fetchone()
            return User(id=result[0],
                        name=result[1],
                        fullName=result[2],
                        passwordHash=result[3],
                        role=result[4])


def get_user_by_name(username: str) -> User:
    with get_database_connection() as conn:
        with conn.cursor() as c:
            c.execute(
                'select id,name,fullName,passwordHash,role from users where name=%s',
                [username])
            result = c.fetchall()[0]
            return User(id=result[0],
                        name=result[1],
                        fullName=result[2],
                        passwordHash=result[3],
                        role=result[4])


def get_users() -> List[User]:
    with get_database_connection() as conn:
        with conn.cursor() as c:
            c.execute('select id,name,fullName,passwordHash,role from users')
            result = c.fetchall()
            return [
                User(id=row[0],
                     name=row[1],
                     fullName=row[2],
                     passwordHash=row[3],
                     role=row[4]) for row in result
            ]


def add_user(name: str, fullName: str, password: str, role: str) -> int:
    with get_database_connection() as conn:
        with conn.cursor() as c:
            c.execute('select count(id) from users where name=%s', [name])
            if c.fetchone()[0] != 0:
                raise UserExistsError(name)
            c.execute(
                'insert into users values (default,%s,%s,%s,%s) returning id',
                [name, fullName, hash_password(password), role])
            return c.fetchone()[0]


def set_password(userid: int, password: str):
    with get_database_connection() as conn:
        with conn.cursor() as c:
            c.execute('update users set passwordHash=%s where id=%s',
                      [hash_password(password), userid])


def update_user(id: int, name: str, fullName: str, password: str, role: str):
    with get_database_connection() as conn:
        with conn.cursor() as c:
            if password is None:
                c.execute(
                    'update users set name=%s,fullName=%s,role=%s where id=%s',
                    [name, fullName, role, id])
            else:
                c.execute(
                    'update users set name=%s,fullName=%s,passwordHash=%s,role=%s where id=%s',
                    [name, fullName,
                     hash_password(password), role, id])


def delete_user(id: int):
    with get_database_connection() as conn:
        with conn.cursor() as c:
            c.execute('delete from users where id=%s', [id])


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return base64.b64encode(hash + salt).decode()


def check_password(password: str, hashstr: str) -> bool:
    hash = base64.b64decode(hashstr.encode())
    old_hash = hash[0:32]
    salt = hash[32:48]
    new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    print(f'old: {old_hash} new: {new_hash}')
    return old_hash == new_hash


def authenticate(username: str, password: str) -> bool:
    try:
        user = get_user_by_name(username)
        return check_password(password, user.passwordHash)
    except Exception as err:
        logging.error(f'authentication failed: {sys.exc_info()} ')
        return False


def is_admin(username: str) -> bool:
    return get_user_by_name(username).role == 'admin'
