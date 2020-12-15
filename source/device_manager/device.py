from uuid import UUID, uuid4
from typing import List
from source.device_manager.device_layer.device_info import DeviceInfo, DeviceStatus
from source.device_manager.device_layer.device_interface import DeviceType
from source.device_manager.device_layer.dynamic_client import delete_dynamic_client
from source.device_manager.database import get_database_connection


def get_device_info_list() -> List[DeviceInfo]:
    """Returns a list of devices information from the database"""
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                'select uuid,name,type,address,port,available,userID,databaseID from devices'
            )
            result = cursor.fetchall()
            return [
                DeviceInfo(row[0], row[1], row[2], row[3], row[4],
                           bool(row[5]), row[6], row[7]) for row in result
            ]


def get_device_info(uuid: UUID) -> DeviceInfo:
    """Returns the specified device info
    Args:
        uuid (uuid.UUID): The unique id of the device
    Returns:
        DeviceInterface: A instancieted Device
    """
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                'select uuid,name,type,address,port,available,userID,databaseID from devices '\
                'where uuid=%s',
                [str(uuid)])
            dev = cursor.fetchone()
            return DeviceInfo(dev[0], dev[1], dev[2], dev[3], dev[4],
                              bool(dev[5]), dev[6], dev[7])


def set_device(device: DeviceInfo):
    """Updates a device in the database
    Args:
        device: The device that should replace the one in the database
    """
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                'update devices set name=%s, type=%s,address=%s,port=%s '\
                'where uuid=%s',
                [
                    device.name, device.type, device.address, device.port,
                    str(device.uuid)
                ])


def add_device(name: str, type: DeviceType, address: str, port: int) -> UUID:
    """Add a new device to the database
    Args:
        device: The new device that should be added to the database
    """
    uuid = uuid4()
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                'insert into devices values (default,%s,%s,%s,%s,%s,%s,%s,%s)',
                [str(uuid), name, type, address, port, True, None, None])
    return uuid


def delete_device(uuid: UUID):
    """Delete a device from the database
    Args:
        uuid (uuid.UUID): The unique id of the device
    """
    device = get_device_info(uuid)
    if device.type == DeviceType.SILA:
        delete_dynamic_client(uuid)
    with get_database_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('delete from devices where uuid=%s', [str(uuid)])