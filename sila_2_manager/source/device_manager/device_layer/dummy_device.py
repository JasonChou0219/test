from source.device_manager.device_layer.device_interface import DeviceInterface, DeviceType
from typing import List, Dict, Any


class DummyDevice(DeviceInterface):
    def __init__(self,
                 ip: str,
                 port: int,
                 uuid,
                 name: str,
                 type: DeviceType = DeviceType.CUSTOM):
        super().__init__(ip, port, uuid, name, type)

    def connect(self):
        pass

    #async def connect_async(self):
    #    pass

    def get_status(self):
        return ""

    def is_online(self):
        return False

    def call_command(self, feature_id: str, command_id: str,
                     parameters: Dict[str, Any]):
        pass

    def call_property(self, feature_id, property_id):
        pass

    def get_feature_names(self) -> List[str]:
        return []

    def get_feature_description(self, feature_id: str):
        pass

    def get_commands(self, feature_id: str):
        return []

    def get_properties(self, feature_id: str):
        return []
