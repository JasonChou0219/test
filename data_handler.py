from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime

scheduler = BackgroundScheduler()
scheduler.start()


def save_commands(*commands_to_call):
    for command_info in commands_to_call:
        command = command_info[0]
        feature = command_info[1]
        device_info = command_info[2]
        print(command.identifier)
        print(feature.identifier)
        print(device_info.uuid)


def save_properties(*properties_to_call):
    for property_info in properties_to_call:
        property = property_info[0]
        feature = property_info[1]
        device_info = property_info[2]
        print(property.identifier)
        print(feature.identifier)
        print(device_info.uuid)


def create_jobs(commands_to_call, properties_to_call):
    for key in commands_to_call.keys():
        scheduler.add_job(save_commands,
                          'interval',
                          seconds=key[0],
                          start_date=datetime.fromtimestamp(key[1]),
                          end_date=datetime.fromtimestamp(key[2]),
                          args=commands_to_call[key])
    for key in properties_to_call.keys():
        scheduler.add_job(save_properties,
                          'interval',
                          seconds=key[0],
                          start_date=datetime.fromtimestamp(key[1]),
                          end_date=datetime.fromtimestamp(key[2]),
                          args=properties_to_call[key])
