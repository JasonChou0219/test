import workflow
import services
from uuid import UUID


def main():
    # devs = [
    #     create_device_instance(info['address'], info['port'], info['uuid'],
    #                            info['name'], info['type'])
    #     for info in devices.devices
    # ]
    # return workflow_script.run(devs)
    print('main.py executed \n')
    return workflow.run()


if __name__ == "__main__":
    main()
