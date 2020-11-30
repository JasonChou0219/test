import sys
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from influxdb import InfluxDBClient

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
                # TODO experiment
                # TODO for a device write all points at the end
                # TODO store to database specified in device
                # TODO timeout call
                # TODO meta / non-meta indicator
                # TODO decide if we need to do something if responses == {}
                # TODO report on different possible exceptions
                # TODO check if possible to make these 2 functions into a single one
                if responses != {}:
                    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'device_manager')
                    client.create_database('device_manager')
                    point = {}
                    tags = {'device': device_uuid, 'feature': feature.identifier, 'command': command.identifier}
                    point['measurement'] = 'device_manager'
                    point['tags'] = tags
                    point['time'] = datetime.now()
                    point['fields'] = responses
                    points = [point]

                    client.write_points(points)
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
                # TODO experiment
                # TODO for a device write all points at the end
                # TODO store to database specified in device
                # TODO timeout call
                # TODO meta / non-meta indicator
                # TODO decide if we need to do something if responses == {}
                # TODO report on different possible exceptions
                # TODO check if possible to make these 2 functions into a single one
                if responses != {}:
                    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'device_manager')
                    client.create_database('device_manager')
                    point = {}
                    tags = {'device': device_uuid, 'feature': feature.identifier, 'property': property.identifier}
                    point['measurement'] = 'device_manager'
                    point['tags'] = tags
                    point['time'] = datetime.now()
                    point['fields'] = responses
                    points = [point]

                    client.write_points(points)
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
