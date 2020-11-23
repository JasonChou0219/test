from source.device_manager.device_layer.device_interface import DeviceInterface, DeviceType, DeviceError
from typing import List, Dict, Any
from source.device_manager.device_layer.dynamic_client import DynamicSiLA2Client
from uuid import UUID
from logging import error
import sys
import traceback
# import asyncio


def create_and_init_dynamic_client(name, ip, port):
    client = None
    try:
        client = DynamicSiLA2Client(name=f'{name}-client',
                                    server_ip=ip,
                                    server_port=port)
        client.run()
    except Exception as e:
        client = None
        print(traceback.print_exc(file=sys.stdout))
        error(f'Could not create DynamicClient for {name}: {sys.exc_info()} ')
    return client


class SilaDevice(DeviceInterface):
    def __init__(self, ip: str, port: int, uuid: UUID, name: str):
        super().__init__(ip, port, uuid, name, DeviceType.SILA)
        self.__client = None
        self.defult_interval = 10

    def connect(self):
        self.__client = create_and_init_dynamic_client(self.name, self.ip,
                                                       self.port)

    def getClient(self) -> DynamicSiLA2Client:
        return self.__client

    def get_description(self):
        client = self.getClient()
        return client.description

    def get_feature_names(self) -> List[str]:
        client = self.getClient()
        return client.list_features()

    def get_feature_description(self, feature_id: str):
        return ''

    def get_feature_path(self, feature_id: str):
        client = self.getClient()
        return client.get_feature_path(feature_id)

    def get_commands(self, feature_id: str):
        client = self.getClient()
        return client.list_property_names(feature_id)

    def get_properties(self, feature_id: str):
        client = self.getClient()
        return client.list_command_names(feature_id)

    def get_status(self):
        return ""

    def is_online(self):
        return self.__client is not None

    def call_command(self, feature_id: str, command_id: str,
                     parameters: Dict[str, Any]):
        client = self.getClient()
        return client.call_command(feature_id, command_id, parameters)

    def call_property(self, feature_id, property_id):
        client = self.getClient()
        return client.call_property(feature_id, property_id)

    def interval_dict(self):
        interval = {}
        for feature in self.get_feature_names():
            for properties in self.get_properties(feature):
                interval[properties] = self.defult_interval
        return interval
