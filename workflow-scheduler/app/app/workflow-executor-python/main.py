import logging
from datetime import datetime
from uuid import UUID

import workflow
import services


# Function to initialize the logging, logs a) to console and b) to file, please note that the file logging will only be
# appended to one single file
def initialize_logging():
    # Initialize logging
    logger_object = logging.getLogger(__name__)
    logger_object.setLevel(logging.DEBUG)
    logger_object.propagate = False

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File handler
    ts = datetime.now()
    filehandler = logging.FileHandler(f'logs/{ts.year}_{ts.month}_{ts.day}_{ts.hour}_{ts.minute}_{ts.second:.0f}_main.log', mode='a')
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)
    logger_object.addHandler(filehandler)

    # Console handler, i.e. output to command window
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger_object.addHandler(console_handler)
    return logger_object


def main():
    # devs = [
    #     create_device_instance(info['address'], info['port'], info['uuid'],
    #                            info['name'], info['type'])
    #     for info in devices.devices
    # ]
    # return workflow_script.run(devs)
    logger = initialize_logging()
    logger.info(f'Logger name: {logging.getLogger(__name__)} \n')
    logger.info('main.py executed \n')
    print('Services are: ', services)

    print('main.py executed \n')
    return workflow.run()


if __name__ == "__main__":
    main()
