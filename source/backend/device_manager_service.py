from uuid import UUID
from dataclasses import asdict
from dacite import from_dict, Config

from source.device_manager.device_layer.device_info import DeviceInfo
from source.device_manager.device_manager import DeviceManager
from source.device_manager.database import get_database_connection
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class NewDatabaseModel(BaseModel):
    name: str
    address: str
    port: int


class DatabaseInfoModel(BaseModel):
    id: int
    name: str
    address: str
    port: int


class DeviceStatusModel(BaseModel):
    online: bool
    status: str


class NewDeviceModel(BaseModel):
    name: str
    type: int
    address: str
    port: int


class DeviceInfoModel(BaseModel):
    uuid: UUID
    name: str
    type: int
    address: str
    port: int
    available: bool = True
    user: Optional[int] = None
    database_id: Optional[int] = None
    active: Optional[bool] = True


class BookingModel(BaseModel):
    name: str
    start: int
    end: int
    user: str
    device: UUID
    experiment: Optional[int] = None


class ExperimentBookingModel(BaseModel):
    name: str
    start: int
    end: int
    devices: List[UUID]
    scriptID: int


class ScriptModel(BaseModel):
    name: str
    fileName: str
    data: str


class ScriptInfoModel(BaseModel):
    name: str
    fileName: str


class DeviceCommandParameter(BaseModel):
    name: str
    value: Any


#class DeviceCommandParameters(BaseModel):
#    params: Dict[str, Any]


class DeviceCommandParameters(BaseModel):
    params: List[DeviceCommandParameter]


class DeviceManagerService:
    def __init__(self):
        self.device_manager = DeviceManager()
        return

    def get_devices(self):
        return [
            asdict(dev) for dev in self.device_manager.get_device_info_list()
        ]

    def get_device(self, uuid: UUID):
        return asdict(self.device_manager.get_device_info(uuid))

    def set_device(self, uuid: UUID, dev):
        self.device_manager.set_device(
            DeviceInfo(dev.uuid, dev.name, dev.type, dev.address, dev.port,
                       dev.available, dev.user))

    def add_device(self, dev):
        self.device_manager.add_device(dev.name, dev.type, dev.address,
                                       dev.port)

    def delete_device(self, uuid: UUID):
        self.device_manager.delete_device(uuid)

    def get_status(self, uuid: UUID):
        return asdict(self.device_manager.get_status(uuid))

    def get_features(self, uuid: UUID):
        return [
            asdict(feature)
            for feature in self.device_manager.get_features(uuid)
        ]

    def get_features_for_data_handler(self, uuid: UUID):
        return [
            asdict(feature) for feature in
            self.device_manager.get_features_for_data_handler(uuid)
        ]

    def call_feature_command(self, device: UUID, feature: str, command_id: str,
                             params: List[DeviceCommandParameter]):
        param_dict = {}
        for param in params:
            param_dict[param.name] = param.value

        return [{
            'name': name.split('/')[0],
            'value': value
        } for name, value in self.device_manager.call_feature_command(
            device, feature, command_id, param_dict).items()]

    def get_feature_property(self, device: UUID, feature: str,
                             property_id: str):
        return [{
            'name': name.split('/')[0],
            'value': value
        } for name, value in self.device_manager.get_feature_property(
            device, feature, property_id).items()]

    def get_databases(self):
        return [
            asdict(database) for database in self.device_manager.get_database_info_list()
        ]

    def get_database_status(self, id: int):
        return asdict(self.device_manager.get_database_status(id))

    def get_database(self, id: int):
        return asdict(self.device_manager.get_database_info(id))

    def add_database(self, database: NewDatabaseModel):
        self.device_manager.add_database(database.name, database.address, database.port)

    def set_database(self, id: int, database: DatabaseInfoModel):
        self.device_manager.set_database(database.id, database.name, database.address, database.port)

    def delete_database(self, id: int):
        self.device_manager.delete_database(id)

    def link_database(self, device_uuid: UUID, database_id: int):
        self.device_manager.link_database(device_uuid, database_id)

    def unlink_database(self, device_uuid: UUID):
        self.device_manager.unlink_database(device_uuid)

    def set_device_attributes_for_data_handler(self, device_uuid: UUID, active: bool):
        self.device_manager.set_device_attributes_for_data_handler(device_uuid, active)

    def discover_sila_devices(self):
        return [
            asdict(dev) for dev in self.device_manager.discover_sila_devices()
        ]

    def get_log(self, from_date: int, to_date: int, exclude=None):
        return self.device_manager.get_log(from_date, to_date, exclude)

    def get_device_bookings(self, device: UUID, start: int, stop: int):
        return [
            asdict(booking_info) for booking_info in self.device_manager.
            get_device_bookings_with_name(device, start, stop)
        ]

    def get_booking_entry(self, id: int):
        return self.device_manager.get_booking_entry(id)

    def get_bookings(self, start: int, stop: int):
        return [
            asdict(booking_info)
            for booking_info in self.device_manager.get_all_bookings_with_name(
                start, stop)
        ]

    def book_device(self, name: str, user: int, device: UUID, start: int,
                    stop: int) -> bool:
        return self.device_manager.book_device(name, user, device, start, stop)

    def delete_booking_entry(self, id: int):
        return self.device_manager.delete_booking_entry(id)

    def get_all_experiments(self):
        return [
            asdict(experiment)
            for experiment in self.device_manager.get_all_experiments()
        ]

    def get_user_experiments(self, user: int):
        return [
            asdict(experiment)
            for experiment in self.device_manager.get_user_experiments(user)
        ]

    def create_experiment(self, name: str, start: int, end: int, user: int,
                          devices: List[UUID], script: int) -> bool:
        return self.device_manager.create_experiment(name, start, end, user,
                                                     devices, script)

    def delete_experiment(self, experimentID: int):
        return self.device_manager.delete_experiment(experimentID)

    def get_user_scripts(self, user: int):
        return [
            asdict(scripts)
            for scripts in self.device_manager.get_user_scripts(user)
        ]

    def get_user_scripts_info(self, user: int):
        return [
            asdict(info)
            for info in self.device_manager.get_user_scripts_info(user)
        ]

    def get_user_script(self, script_id: int):
        return self.device_manager.get_user_script(script_id)

    def get_user_script_info(self, script_id: int):
        return self.device_manager.get_user_script_info(script_id)

    def create_user_script(self, name: str, file_name: str, user: int,
                           data: str) -> int:
        return self.device_manager.create_user_script(name, file_name, user,
                                                      data)

    def delete_user_script(self, script_id: int):
        return self.device_manager.delete_user_script(script_id)

    def set_user_script_info(self, script_id: int, name: str, file_name: str,
                             user: int):
        return self.device_manager.set_user_script_info(
            script_id, name, file_name, user)

    def set_user_script(self, script_id: int, name: int, file_name: str,
                        user: int, data: str):
        return self.device_manager.set_user_script(script_id, name, file_name,
                                                   user, data)
