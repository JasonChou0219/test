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
        'name': 'Tutorial 1 Hello SiLA 2 Manager!',
        'fileName': 'Tutorial_1_Hello_SiLA_2_Manager.py',
        'user': 1,
        'data': '""" \n'
                'TUTORIAL 1: Hello_SiLA_2_Manager \n'
                '--------------------------------------------- \n'
                '1.1 You can use this code editor like a regular scripting environment.  \n'
                '\t If you require specific python packages for your script, you can import them here. \n'
                ' \n'
                'Hint 1: Packages you want to import must be specified in the dockerfiles requirements.txt! \n'
                '\t The file is located in your SiLA 2 Manager Installation directory. The default location \n'
                '\t on Linux is /home/<your_username>/sila2_device_manager/user_script_env/requirements.txt. \n'
                '\t If you change the requirements, you need to rerun the create_container.sh to update the  \n'
                '\t docker container image. \n'
                '""" \n'
                ' \n'
                'import sys \n'
                'import time \n'
                'import numpy as np \n'
                ' \n'
                '""" \n'
                '1.2 You can use the python logging package and configure the output format here. Logging statements  \n'
                '\t are transferred via the stderr of the docker container and are flushed by default by the logging  \n'
                '\t function. All output is forwarded to the SiLA 2 Manager frontend. You can display the logs in the  \n'
                '\t "experiments"-tab by clicking on an experiment. \n'
                '\t When an script crashes straight-away, the logs may fail to arrive at the frontend so you have to  \n'
                '\t open the files directly. \n'
                '\t The log files are stored locally on your computer: \n'
                '\t Linux:   /tmp/device_manager/container \n'
                '\t Windows: C:/Users<your_username>/AppData/Local/Temp/device-manager/container \n'
                '""" \n'
                ' \n'
                'import logging \n'
                "logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG) \n"
                'logger = logging.getLogger(name=__name__) \n'
                ' \n'
                '""" \n'
                '1.3 When the experiment is started, the function run() is called. Therefore, every script must  \n'
                '\t contain a run() function. The run function requires one argument: services. This argument  \n'            
                '\t is used to pass the SiLA Server clients information into the script. You have to supply this \n'
                '\t argument, even if you don\'t use it! \n'      
                ' \n'
                'Hint 2: Use the flush argument when using print statements or add a newline character (\\n) to the  \n'
                '\t end of your string. Logging statements are flushed automatically. \n'
                '""" \n'            
                ' \n'
                ' \n'
                'def run(services): \n'   
                '\t """ Required to import and instantiate devices """ \n'
                '\t \n'
                "\t print('Hello SiLA2 Manager') \n"
                '\t # The above print statement will not be shown in the experiment terminal before the statement below is executed and flushed.\n'            
                '\t time.sleep(5)  \n'
                "\t print('Yay me, i got flushed!', flush=True) \n"   
                "\t print(f'A random number: {np.random.rand()}', flush=True) \n"
                '\t \n'
                '\t write_logging_statement() \n'
                '\t write_to_output() \n'   
                ' \n'
                '""" \n'
                '1.4 You can call other functions from within thr run() function. The function "write_logging_statement" \n'   
                '\t writes logging statements of all available log_levels. \n'
                '""" \n'   
                ' \n'
                ' \n'
                'def write_logging_statement(): \n'   
                '\t """Writes logging statements""" \n'
                '\t time.sleep(1) \n'
                "\t logger.debug('A debug statement') \n"
                '\t time.sleep(1) \n'   
                "\t logger.info('An info statement') \n"
                '\t time.sleep(1) \n'   
                "\t logger.warning('A warning statement') \n"
                '\t time.sleep(1) \n'   
                "\t logger.critical('A critical warning statement') \n"
                '\t time.sleep(1) \n'   
                "\t logger.error('An error statement\\n') \n"
                '\t time.sleep(3) \n'   
                ' \n'
                '""" \n'   
                '1.5 If direct calls to stdout and stderr are made, they won\'t get flushed either. Output has to be flushed explicitly. \n'
                ' \n'   
                'Hint 2: Use the flush argument when using print statements and the sys.stderr.flush and sys.stdout.flush function for  \n'
                '\t write operations with sys. \n'
                '""" \n'
                ' \n'   
                ' \n'
                'def write_to_output(): \n'   
                '\t """Writes message to stderr""" \n'
                "\t sys.stderr.write('Error\\n') \n"   
                '\t sys.stderr.flush() \n'
                '\t time.sleep(1) \n'   
                "\t sys.stdout.write('All Good\\n') \n"   
                '\t sys.stdout.flush() \n'
                ' \n'
    },
    {
        'name': 'Tutorial 2 Incorporating SiLA 2 Services',
        'fileName': 'Tutorial_2_Incorporating_SiLA_Services.py',
        'user': 1,
        'data': '""" \n'
                'TUTORIAL 2: Incorporating SiLA 2 Services \n'
                '--------------------------------------------- \n'
                '\n'
                'This example uses the SiLA Python HelloSiLA_Full example server. \n'
                'You can download it from the repository at https://gitlab.com/SiLA2/sila_python/-/tree/master/examples/HelloSiLA2/HelloSiLA2_Full \n'
                '\n'
                'To run this example follow these steps: \n'
                '\n'
                '2.1. Add a SiLA Server to your Services (Ideally the HelloSiLA example from the SiLA Python or Tecan repository) \n'
                '2.2. Go to the Data Handler tab and deactivate the "Active" checkbox for the device you want to use \n'
                '2.3. Set up an experiment with and select this script and the device you want to use \n'
                '2.4. Hit the run button or wait for the scheduled execution time (You can click on the experiment \n'
                '\t name to get the docker container stdout, i.e the output of your script) \n'
                '\n'
                'Hint 1: The def run() method is compulsory. The services are passed to it in the same order, \n'
                '\t that you select them in during experiment setup, i.e the order they are displayed in in\n'
                '\t the experiment list entry of you experiment\n'
                '\n'
                'Hint 2: Use the flush argument when using print statements. \n'
                '\n'
                'Hint 3: The command/property call syntax is displayed in the "Services" tab. It is shown under \n'
                '\t "Usage" on the lowest level of the device tree for every command and property. \n'
                '""" \n'
                '\n'
                'import time \n'
                '\n'
                'def run(services): \n'
                '\t """ Instantiates selected devices for this experiment """ \n'
                '\t client = services[0] \n'
                "\t print(f'Service instantiated: {client.name}@{client.ip}:{client.port}', flush=True) \n"
                '\t client.connect() \n'
                '\t # A GET command. A call to the SiLAService feature. Request the server name. \n'
                '\t for i in range(10): \n'
                '\t \t response = client.call_property("SiLAService\\n", "ServerName") \n'
                '\t \t print(response, flush=True) \n'
                '\t \t time.sleep(2)\n'
                '\t \n'
                '\t # A Set command. A call to the SiLAService feature. Change the server name. \n'
                '\t client.call_command("SiLAService\\n","SetServerName", parameters={"ServerName/constrained/String": "MyNewName"}) \n'
                '\t response = client.call_property("SiLAService\\n", "ServerName") \n'
                "\t print('Changed name to: ', response, flush=True) \n"
                '\t # Change the ServerName back to the original one \n'
                '\t client.call_command("SiLAService\\n","SetServerName", parameters={"ServerName/constrained/String": ServerName}) \n'
                '\t # Change the ServerName back to the original one\n'
                '\t response = client.call_property("SiLAService\\n", "ServerName") \n'
                "\t print('Changed name back to:', response, flush=True) \n"
                '\n'
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
              'display_name varchar(256), ' \
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
              'display_name varchar(256), ' \
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
              'display_name varchar(256), ' \
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
              'display_name varchar(256), ' \
              'description text, ' \
              'data_type varchar(256), ' \
              'value varchar(256), ' \
              # Should be 'parameter' if it is a parameter, 'response' if it is a response
              # or 'intermediate' if it is an intermediate
              'used_as varchar(256), ' \
              # Should be 'command' if it belongs to a command or 'property' if it belongs to a property
              'parent_type varchar(256), ' \
              # The id of the parent command or feature
              'parent integer)')


def add_responses_for_data_handler(c):
    c.execute('create table if not exists responses_for_data_handler ' \
              '(id serial primary key, ' \
              'identifier varchar(256), ' \
              'display_name varchar(256), ' \
              'description text, ' \
              'data_type varchar(256), ' \
              'value varchar(256), ' \
              # Should be 'parameter' if it is a parameter, 'response' if it is a response
              # or 'intermediate' if it is an intermediate
              'used_as varchar(256), ' \
              # Should be 'command' if it belongs to a command or 'property' if it belongs to a property
              'parent_type varchar(256), ' \
              # The id of the parent command or feature
              'parent integer)')


def add_intermediate_responses_for_data_handler(c):
    c.execute('create table if not exists intermediate_responses_for_data_handler ' \
              '(id serial primary key, ' \
              'identifier varchar(256), ' \
              'display_name varchar(256), ' \
              'description text, ' \
              'data_type varchar(256), ' \
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
    add_responses_for_data_handler(c)
    add_intermediate_responses_for_data_handler(c)
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
