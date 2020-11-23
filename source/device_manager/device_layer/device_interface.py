from abc import ABC, abstractmethod
from typing import List, Dict, Any
import sqlite3
from enum import IntEnum
from dataclasses import dataclass
from uuid import UUID


class DeviceType(IntEnum):
    SILA = 0,
    CUSTOM = 1,
    SOFT = 1


class DeviceError(Exception):
    def __init__(self, ip: str, port: int, uuid: UUID, name: str,
                 type: DeviceType, *args):
        self.ip = ip
        self.port = port
        self.uuid = uuid
        self.name = name
        self.type = type


class DeviceInterface(ABC):
    @abstractmethod
    def __init__(self, ip: str, port: int, uuid: UUID, name: str,
                 type: DeviceType):
        self.ip = ip
        self.port = port
        self.uuid = uuid
        self.name = name
        self.type = type

    @abstractmethod
    def connect(self):
        pass

    #@abstractmethod
    #async def connect_async(self):
    #    pass

    @abstractmethod
    def get_status(self):
        pass

    @abstractmethod
    def is_online(self) -> bool:
        pass

    @abstractmethod
    def get_feature_names(self) -> List[str]:
        pass

    @abstractmethod
    def get_feature_description(self, feature_id: str):
        pass

    @abstractmethod
    def get_commands(self, feature_id: str):
        pass

    @abstractmethod
    def get_properties(self, feature_id: str):
        pass

    @abstractmethod
    def call_command(self, feature_id: str, command_id: str,
                     parameters: Dict[str, Any]):
        pass
