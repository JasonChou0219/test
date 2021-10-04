from source.device_manager.device_layer.device_interface import DeviceInterface, DeviceType
from source.device_manager.device_layer.sila_device import SilaDevice
from source.device_manager.device_layer.dummy_device import DummyDevice
import script
import devices
from uuid import UUID


def create_device_instance(ip: str, port: int, uuid: UUID, name: str,
                           type: DeviceType):
    if type == DeviceType.SILA:
        return SilaDevice(ip, port, uuid, name)
    else:
        return DummyDevice(ip, port, uuid, name, type)


def main():

    devs = [
        create_device_instance(info['address'], info['port'], info['uuid'],
                               info['name'], info['type'])
        for info in devices.devices
    ]
    return script.run(devs)


if __name__ == "__main__":
    main()
