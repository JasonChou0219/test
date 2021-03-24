#!/usr/bin/env python3
import psycopg2
from os import path, remove, system
from uuid import UUID, uuid4

from source.device_manager.user import hash_password, check_password
from source.device_manager.device_log import LogLevel, LogEntry
from source.device_manager.device_layer.device_interface import DeviceType
from source.device_manager.data_directories import create_directories
from datetime import datetime
from hashlib import sha256

devices = [{
    'uuid': uuid4(),
    'server_uuid': uuid4(),
    'name': "Dummy Device 1",
    'type': DeviceType.SILA,
    'address': "192.168.0.20",
    'port': 50001,
    'available': True,
    'user': None
}, {
    'uuid': uuid4(),
    'server_uuid': uuid4(),
    'name': "Dummy Device 2",
    'type': DeviceType.CUSTOM,
    'address': "192.168.0.25",
    'port': 55001,
    'available': False,
    'user': 1
}, {
    'uuid': uuid4(),
    'server_uuid': uuid4(),
    'name': "Dummy Device 3",
    'type': DeviceType.SILA,
    'address': "192.168.0.40",
    'port': 50002,
    'available': True,
    'user': None
}]

users = [{
    'name': 'admin',
    'fullName': 'administrator',
    'passwordHash': hash_password(sha256(b'1234').hexdigest()),
    'role': 'admin'
}, {
    'name': 'user1',
    'fullName': 'Max Mustermann',
    'passwordHash': hash_password(sha256(b'asdf').hexdigest()),
    'role': 'user'
}]

logs = [
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('01-04-2020 08:54:22',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('01-04-2020 09:12:02',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('01-04-2020 11:20:55',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.At vero eos et accusam et justo duo dolores et ea rebum.Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.At vero eos et accusam et justo duo dolores et ea rebum.Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('01-04-2020 12:02:08',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Very long Device Name',
        'time':
        int(
            datetime.strptime('01-04-2020 18:54:30',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.WARNING,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 09:20:01',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Something',
    },
    {
        'type':
        LogLevel.CRITICAL,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 10:49:42',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Something',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 14:35:59',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 14:35:10',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 14:35:10',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.ERROR,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 14:35:10',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Overheat',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 14:35:10',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('01-04-2020 08:54:22',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('01-04-2020 08:54:22',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('01-04-2020 08:54:22',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('01-04-2020 09:12:02',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('01-04-2020 11:20:55',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.At vero eos et accusam et justo duo dolores et ea rebum.Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.At vero eos et accusam et justo duo dolores et ea rebum.Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('01-04-2020 12:02:08',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Very long Device Name',
        'time':
        int(
            datetime.strptime('01-04-2020 18:54:30',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.WARNING,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 09:20:01',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Something',
    },
    {
        'type':
        LogLevel.CRITICAL,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 10:49:42',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Something',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 14:35:59',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 14:35:10',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 14:35:10',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.ERROR,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 14:35:10',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Overheat',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('02-04-2020 14:35:10',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('01-04-2020 08:54:22',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
    {
        'type':
        LogLevel.INFO,
        'device':
        'Device 1',
        'time':
        int(
            datetime.strptime('01-04-2020 08:54:22',
                              '%d-%m-%Y %H:%M:%S').timestamp()),
        'message':
        'Device Init',
    },
]

booking_info = [{
    'name':
    'experiment1',
    'start':
    int(
        datetime.strptime('19-09-2020 08:54:22',
                          '%d-%m-%Y %H:%M:%S').timestamp()),
    'end':
    int(
        datetime.strptime('20-09-2020 09:54:22',
                          '%d-%m-%Y %H:%M:%S').timestamp()),
    'user':
    1,
    'device':
    devices[0]['uuid'],
    'experiment':
    1
}]

experiments = [{
    'name':
    'Experiment 1',
    'start':
    int(
        datetime.strptime('19-09-2020 08:54:22',
                          '%d-%m-%Y %H:%M:%S').timestamp()),
    'end':
    int(
        datetime.strptime('20-09-2020 09:54:22',
                          '%d-%m-%Y %H:%M:%S').timestamp()),
    'user':
    1,
    'script':
    1
}]

scripts = [
    {
        'name': 'Hello device!',
        'fileName': 'Hello_device.py',
        'user': 1,
        'data': '# You can use this code editor like a regular scripting environment. \n'
                '# If you require specific python packages for your script, you can import them here. \n'
                '# Note: Packages you want to import must be specified in the dockerfiles requirements.txt! \n\n'
                'import time\n\n'
                'def run(devices):\n'
                '    """ Required to import and instantiate devices """\n'
                '    return\n\n'
                '# Print statements do not get flushed, so they will not be forwarded to the frontend terminal straight away. This is a docker limitation\n'
                "print(\'I will get printed with the following print statement. Check my timestamp!\')\n"
                '# This problem can be circumvented by setting the flush attribute to true\n'
                'time.sleep(3)\n'
                "print(\'Yay me, i got flushed!\', flush=True)\n"
                'time.sleep(3)\n\n'
                '# If direct calls to stdout and stderr are made, they won\'t get flushed either. Output has to be flushed explicitly.\n'
                'import sys\n'
                "sys.stderr.write(\'Error\\n\')\n"
                'sys.stderr.flush()\n'
                'time.sleep(1)\n'
                "sys.stdout.write(\'All Good\\n\')\n"
                'sys.stdout.flush()\n'
                'time.sleep(3)\n\n'
                '# If logging is used, this problem doesn\'t arise. Logging statements are transferred via stderr and are flushed by default by the logging function.\n'
                'import logging\n'
                "logging.basicConfig(format=\'%(levelname)-8s| %(module)s.%(funcName)s: %(message)s\', level=logging.DEBUG)\n"
                'logger = logging.getLogger(name=__name__)\n'
                "logger.debug('A debug statement')\n"
                "logger.info('An info statement')\n"
                "logger.warning('A warning statement')\n"
                "logger.critical('A critical warning statement')\n"
                "logger.error('An error statement')\n"
    },
    {
        'name': 'Device example',
        'fileName': 'device_example.py',
        'user': 1,
        'data': '# WIP\n'
                '# This example will show you how to import a device client\n'
                '# This is work in progress\n\n'
                '# ...\n\n'
                '# You can call functions as described for every command and property in the device feature explorer under "Usage"\n'
                '# To call the property "StartYear" of the HelloSiLA example device use:\n'
                'StartYear = yourObject.call_property("GreetingProvider","StartYear")\n\n'
                '# To run the "SayHello" command use:\n'
                'response = yourObject.call_command("GreetingProvider","SayHello",parameters={"Name": \'some name\'})\n\n'
                '# Note: you need to replace the "yourObject" part of the command with the client object of that device!'
    },
    {
        'name': 'InfluxDB example',
        'fileName': 'influx_example.py',
        'user': 1,
        'data': 'from influxdb import InfluxDBClient\n'
                'from datetime import datetime\n'
                'import numpy as np\n\n\n'
                'import time'
                '# Instantiate the database client.\n'
                'influx_client = InfluxDBClient(host=\'localhost\', port=8086, username=\'root\', password=\'root\', database=\'device_manager\')\n\n'
                '# Check connection\n'
                'print(f\'Checking connectivity. DB server version: {influx_client.ping()}\')\n\n'
                'for i in range(0, 100, 1):\n'
                '\t# This is an example write operation\n'
                '\tdata_point = {\n'
                '\t\t"measurement": "testMeasurement",\n'
                '\t\t"tags": {\n'
                '\t\t\t"experiment_name": "influxDB_test"\n'
                '\t\t},\n'
                '\t\t"time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),\n'
                '\t\t"fields": {\n'
                '\t\t\t"test_number": np.random.rand(1)\n'
                '\t\t}\n'
                '\t}\n'
                '\t try:\n'
                '\t\tinflux_client.write_point([data_point])\n'
                '\texcept:\n'
                '\t\t print("This did not work...")\n\n'
                '\t# This is an example query.\n'
                '\tresults = influx_client.query(\n'
                '\t\t\'SELECT test_number FROM "device_manager"."autogen"."testMeasurement" WHERE experiment_name = \\\'influxDB_test\\\' GROUP BY position \n\''
                '\t\t\'ORDER BY DESC LIMIT 1\')\n'
                '\tprint(results)\n\n'
                '\ttime.sleep(10)\n'
    }
]


def add_user(c):
    c.execute('create table if not exists users '\
            '(id serial primary key, '\
            'name varchar(256), '\
            'fullName varchar(256), '\
            'passwordHash varchar(1024),' \
            'role varchar(256))')

    for user in users:
        c.execute('insert into users values (default,%s,%s,%s,%s)', [
            user['name'], user['fullName'], user['passwordHash'], user['role']
        ])


def add_devices(c):
    c.execute('create table if not exists devices '\
            '(id serial primary key, '\
            'uuid UUID, '\
            'server_uuid UUID, '\
            'name varchar(256), '\
            'type integer, '\
            'address varchar(256), '\
            'port integer,' \
            'available boolean, ' \
            'userID integer, ' \
            'databaseID integer, ' \
            'activated boolean)')
    for device in devices:
        c.execute('insert into devices values (default,%s,%s,%s,%s,%s,%s,%s,%s)',
                  [
                      str(device['uuid']), str(device['server_uuid']), device['name'], device['type'],
                      device['address'], device['port'], device['available'],
                      device['user']
                  ])


def add_features_for_data_handler(c):
    c.execute('create table if not exists features_for_data_handler ' \
              '(id serial primary key, ' \
              'identifier varchar(256), ' \
              'name varchar(256), ' \
              'description text, ' \
              'sila2_version varchar(256), ' \
              'originator varchar(256), ' \
              'category varchar(256), ' \
              'maturity_level varchar(256), ' \
              'locale varchar(256), ' \
              'feature_version varchar(256), ' \
              'feature_version_major integer, ' \
              'feature_version_minor integer, ' \
              'device UUID, ' \
              'activated boolean, ' \
              'meta boolean)')


def add_commands_for_data_handler(c):
    c.execute('create table if not exists commands_for_data_handler ' \
              '(id serial primary key, ' \
              'identifier varchar(256), ' \
              'name varchar(256), ' \
              'description text, ' \
              'observable boolean, ' \
              'polling_interval_non_meta integer, ' \
              'polling_interval_meta integer, ' \
              'activated boolean, ' \
              'meta boolean, ' \
              'feature integer)')


def add_properties_for_data_handler(c):
    c.execute('create table if not exists properties_for_data_handler ' \
              '(id serial primary key, ' \
              'identifier varchar(256), ' \
              'name varchar(256), ' \
              'description text, ' \
              'observable boolean, ' \
              'polling_interval_non_meta integer, ' \
              'polling_interval_meta integer, ' \
              'activated boolean, ' \
              'meta boolean, ' \
              'feature integer)')


def add_parameters_for_data_handler(c):
    c.execute('create table if not exists parameters_for_data_handler ' \
              '(id serial primary key, ' \
              'identifier varchar(256), ' \
              'name varchar(256), ' \
              'description text, ' \
              'type varchar(256), ' \
              'value varchar(256), ' \
              # Should be 'parameter' if it is a parameter, 'response' if it is a response
              # or 'intermediate' if it is an intermediate
              'used_as varchar(256), ' \
              # Should be 'command' if it belongs to a command or 'property' if it belongs to a property
              'parent_type varchar(256), ' \
              # The id of the parent command or feature
              'parent integer)')


def add_defined_execution_errors(c):
    c.execute('create table if not exists defined_execution_errors ' \
              '(id serial primary key, ' \
              'defined_execution_error text, ' \
              # Should be 'command' if it belongs to a command or 'property' if it belongs to a property
              'parent_type varchar(256), ' \
              # The id of the parent command or feature
              'parent integer)')


def add_databases(c):
    c.execute('create table if not exists databases ' \
              '(id serial primary key, ' \
              'name varchar(256), ' \
              'address varchar(256), ' \
              'port integer,'
              'username varchar(256),'
              'password varchar(256))')


def add_logs(c):
    c.execute('create table if not exists log'\
            '(id serial primary key, '\
            'type integer, '\
            'device varchar(256), '\
            'time integer, '\
            'message text)')

    for log in logs:
        c.execute('insert into log values (default,%s,%s,%s,%s)',
                  [log["type"], log["device"], log["time"], log["message"]])


def add_booking_info(c):
    c.execute('create table if not exists bookings'\
            '(id serial primary key, '\
            'name varchar(256), '\
            'startTime integer,'\
            'endTime integer,'\
            'userID integer,'\
            'device UUID,'\
            'experiment integer)')
    for entry in booking_info:
        c.execute('insert into bookings values (default,%s,%s,%s,%s,%s,%s)', [
            entry["name"],
            entry["start"],
            entry["end"],
            entry["user"],
            str(entry["device"]),
            entry["experiment"],
        ])


def add_experiments(c):
    c.execute('create table if not exists experiments'\
            '(id serial primary key, '\
            'name varchar(256), '\
            'startTime integer,'\
            'endTime integer,'\
            'userID integer,'\
            'script int)')
    for entry in experiments:
        c.execute('insert into experiments values (default,%s,%s,%s,%s,%s)', [
            entry["name"], entry["start"], entry["end"], entry["user"],
            entry["script"]
        ])


def add_scripts(c):
    c.execute('create table if not exists scripts'\
            '(id serial primary key, '\
            'name varchar(256), '\
            'fileName varchar(256), '\
            'userID integer,'\
            'data text)')
    for entry in scripts:
        c.execute(
            'insert into scripts values (default,%s,%s,%s,%s)',
            [entry["name"], entry["fileName"], entry["user"], entry["data"]])


def main():
    conn = psycopg2.connect(host='localhost',
                            port=5432,
                            user='postgres',
                            password='1234')
    c = conn.cursor()
    add_user(c)
    add_devices(c)
    add_features_for_data_handler(c)
    add_commands_for_data_handler(c)
    add_properties_for_data_handler(c)
    add_parameters_for_data_handler(c)
    add_defined_execution_errors(c)
    add_databases(c)
    add_logs(c)
    add_booking_info(c)
    add_experiments(c)
    add_scripts(c)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
