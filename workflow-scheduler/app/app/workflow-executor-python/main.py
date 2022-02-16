# from source.device_manager.device_layer.device_interface import DeviceInterface, DeviceType
# from source.device_manager.device_layer.sila_device import SilaDevice
# from source.device_manager.device_layer.dummy_device import DummyDevice
import workflow_script
import services
from uuid import UUID


def main():
    # devs = [
    #     create_device_instance(info['address'], info['port'], info['uuid'],
    #                            info['name'], info['type'])
    #     for info in devices.devices
    # ]
    # return workflow_script.run(devs)
    return workflow_script.run()

if __name__ == "__main__":
    main()
