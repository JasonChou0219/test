import sys
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from source.device_manager import device_manager

scheduler = BackgroundScheduler()
scheduler.start()


def save_commands(commands_to_call):
    for device_uuid in commands_to_call.keys():

        dev_manager = device_manager.DeviceManager()
        sila_device = dev_manager.get_device_instance(device_uuid)
        sila_device.connect()

        for command_info in commands_to_call[device_uuid]:

            command = command_info[0]
            feature = command_info[1]

            parameters = {}
            for parameter in command.parameters:
                parameters[parameter.identifier.lower() + '/' + parameter.type] = parameter.value

            try:
                responses = sila_device.call_command(feature_id=feature.identifier+'\n', command_id=command.identifier,
                                                     parameters=parameters)
                print(responses)
            except:
                print(sys.exc_info())


def save_properties(properties_to_call):
    for device_uuid in properties_to_call.keys():

        dev_manager = device_manager.DeviceManager()
        sila_device = dev_manager.get_device_instance(device_uuid)
        sila_device.connect()

        for property_info in properties_to_call[device_uuid]:

            property = property_info[0]
            feature = property_info[1]

            try:
                responses = sila_device.call_property(feature_id=feature.identifier+'\n',
                                                      property_id=property.identifier)
                print(responses)
            except:
                print(sys.exc_info())


def create_jobs(commands_to_call, properties_to_call):
    for key in commands_to_call.keys():
        scheduler.add_job(save_commands,
                          'interval',
                          seconds=key[0],
                          start_date=datetime.fromtimestamp(key[1]),
                          end_date=datetime.fromtimestamp(key[2]),
                          args=[commands_to_call[key]])
    for key in properties_to_call.keys():
        scheduler.add_job(save_properties,
                          'interval',
                          seconds=key[0],
                          start_date=datetime.fromtimestamp(key[1]),
                          end_date=datetime.fromtimestamp(key[2]),
                          args=[properties_to_call[key]])
