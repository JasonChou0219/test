from typing import List, Dict
from uuid import UUID, uuid4
from datetime import datetime

from source.device_manager.sila_auto_discovery.sila_auto_discovery import find
from source.device_manager.device_layer.device_info import DeviceInfo, DeviceStatus
from source.device_manager.device_layer.device_interface import DeviceInterface, DeviceType, DeviceError
from source.device_manager.device_layer.dummy_device import DummyDevice
from source.device_manager.device_layer.sila_device import SilaDevice
from source.device_manager.device_layer.device_feature import DeviceFeature, DeviceFeatureForDataHandler, \
    DeviceCommandForDataHandler, DeviceParameterForDataHandler, DevicePropertyForDataHandler
from source.device_manager.device_layer.sila_feature import serialize_feature
from source.device_manager.device_log import DeviceManagerLogHandler, LogLevel
from source.device_manager.database import get_database_connection
from source.device_manager.scheduler import BookingInfo, get_booking_entry, get_device_booking_info, get_booking_info, book, id_is_valid, delete_booking_entry
from source.device_manager.scheduler import BookingInfoWithNames, get_device_booking_info_with_names, get_booking_info_with_names
from source.device_manager.device_layer.dynamic_client import delete_dynamic_client
import source.device_manager.experiment as experiment
import source.device_manager.script as script

from sila2lib.fdl_parser.fdl_parser import FDLParser
from dataclasses import asdict
from multiprocessing import Process, Pipe

import logging

logger = logging.getLogger()
logger.addHandler(DeviceManagerLogHandler(logging.WARNING))

INTERVAL = 30
META_INTERVAL = 3600
ACTIVATED = True
META = False


def _call_feature_command_from_subprocess(info: DeviceInfo, feature: str,
                                          command: str, parameters: Dict[str,
                                                                         any],
                                          connection):
    try:
        device = _create_device_instance(info.address, info.port, info.uuid,
                                         info.name, info.type)
        device.connect()
        result = device.call_command(feature+'\n', command, parameters)
        connection.send(result)
    finally:
        connection.close()


def _get_feature_property_from_subprocess(info: DeviceInfo, feature: str,
                                          prop: str, connection):
    try:
        device = _create_device_instance(info.address, info.port, info.uuid,
                                         info.name, info.type)
        device.connect()
        result = device.call_property(feature+'\n', prop)
        connection.send(result)
    finally:
        connection.close()


def _create_device_instance(ip: str, port: int, uuid: UUID, name: str, type: DeviceType):
    if type == DeviceType.SILA:
        return SilaDevice(ip, port, uuid, name)
    else:
        return DummyDevice(ip, port, uuid, name, type)


def _get_device_instance_from_subprocess(info: DeviceInfo, connection):
    """Get a device instance for the device specified by the provided details
    """
    try:
        device = _create_device_instance(info.address, info.port, info.uuid, info.name, info.type)
        connection.send(device)
    finally:
        connection.close()


def _get_device_status_from_subprocess(info: DeviceInfo, connection):
    """Get the current status of the specified device
    """
    try:
        device = _create_device_instance(info.address, info.port, info.uuid,
                                         info.name, info.type)
        device.connect()
        connection.send(DeviceStatus(device.is_online(), device.get_status()))
    finally:
        connection.close()


def _get_device_features_from_subprocess(info: DeviceInfo, connection):
    """Get the description of supported features of the specified device
    """
    try:
        device = _create_device_instance(info.address, info.port, info.uuid,
                                         info.name, info.type)
        device.connect()
        features = []
        if device.is_online() and device.type == DeviceType.SILA:
            for name in device.get_feature_names():
                feature_file = device.get_feature_path(name)
                parser = FDLParser(feature_file)
                features.append(serialize_feature(parser))
        connection.send(features)
    finally:
        connection.close()


class DeviceManager:
    """ Device Manager Implementation"""
    def __init__(self):
        """ Device Manager Implementation
        Args:
            conn (sqlite3.Connection): The connection to the database
        """
        self.conn = get_database_connection()

    def get_device_info_list(self) -> List[DeviceInfo]:
        """Returns a list of devices information from the database"""
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select uuid,name,type,address,port,available,userID from devices'
                )
                result = cursor.fetchall()
                return [
                    DeviceInfo(row[0], row[1], row[2], row[3], row[4],
                               bool(row[5]), row[6]) for row in result
                ]

    def get_device_info(self, uuid: UUID) -> DeviceInfo:
        """Returns the specified device info
        Args:
            uuid (uuid.UUID): The unique id of the device
        Returns:
            DeviceInterface: A instancieted Device
        """
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select uuid,name,type,address,port,available,userID from devices '\
                    'where uuid=%s',
                    [str(uuid)])
                dev = cursor.fetchone()
                return DeviceInfo(dev[0], dev[1], dev[2], dev[3], dev[4],
                                  bool(dev[5]), dev[6])

    def set_device(self, device: DeviceInfo):
        """Updates a device in the database
        Args:
            device: The device that should replace the one in the database
        """
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'update devices set name=%s, type=%s,address=%s,port=%s '\
                    'where uuid=%s',
                    [
                        device.name, device.type, device.address, device.port,
                        str(device.uuid)
                    ])

    def add_device(self, name: str, type: DeviceType, address: str, port: int):
        """Add a new device to the database
        Args:
            device: The new device that should be added to the database
        """
        uuid = uuid4()
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'insert into devices values (default,%s,%s,%s,%s,%s,%s,%s,%s)',
                    [str(uuid), name, type, address, port, True, None, None])
        self.add_features_for_data_handler(uuid)

    def delete_device(self, uuid: UUID):
        """Delete a device from the database
        Args:
            uuid (uuid.UUID): The unique id of the device
        """
        device = self.get_device_info(uuid)
        if device.type == DeviceType.SILA:
            delete_dynamic_client(uuid)
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute('delete from devices where uuid=%s',
                               [str(uuid)])

    def get_status(self, uuid: UUID) -> DeviceStatus:
        """Get the current status of the specified device
        Args:
            uuid (uuid.UUID): The unique id of the device
        """
        device_info = self.get_device_info(uuid)
        parent_conn, child_conn = Pipe()
        process = Process(target=_get_device_status_from_subprocess,
                          args=(device_info, child_conn))
        device_status = None
        try:
            process.start()
            device_status = parent_conn.recv()
            process.join()
        finally:
            process.close()
            print('get_status process finished')
        return device_status

    def get_device_instance(self, uuid: UUID):
        """Get a device instance for the specified device
        Args:
        uuid (uuid.UUID): The unique id of the device
        """
        device_info = self.get_device_info(uuid)
        parent_conn, child_conn = Pipe()
        process = Process(target=_get_device_instance_from_subprocess,
                          args=(device_info, child_conn))
        try:
            process.start()
            sila_device = parent_conn.recv()
            process.join()
        finally:
            process.close()
        return sila_device

    def get_features(self, uuid: UUID) -> List[DeviceFeature]:
        """Get the description of supported features of the specified device
        Args:
            uuid (uuid.UUID): The unique id of the device
        """
        device_info = self.get_device_info(uuid)
        parent_conn, child_conn = Pipe()
        process = Process(target=_get_device_features_from_subprocess,
                          args=(device_info, child_conn))
        device_features = None
        try:
            process.start()
            device_features = parent_conn.recv()
            process.join()
        finally:
            process.close()
            print('get_features process finished')
        return device_features

    def call_feature_command(self, device: UUID, feature: str, command: str,
                             params: Dict[str, any]):
        device_info = self.get_device_info(device)
        parent_conn, child_conn = Pipe()
        process = Process(target=_call_feature_command_from_subprocess,
                          args=(device_info, feature, command, params,
                                child_conn))
        result = None
        try:
            process.start()
            result = parent_conn.recv()
            process.join()
        finally:
            process.close()
            print('call_feature_command process finished')
        return result

    def get_feature_property(self, device: UUID, feature: str, prop: str):
        device_info = self.get_device_info(device)
        parent_conn, child_conn = Pipe()
        process = Process(target=_get_feature_property_from_subprocess,
                          args=(device_info, feature, prop, child_conn))
        result = None
        try:
            process.start()
            result = parent_conn.recv()
            process.join()
        finally:
            process.close()
            print('get_feature_property process finished')
        return result

    def add_features_for_data_handler(self, uuid: UUID):
        """Add the features of the device (specified by uuid) to the database
        Args:
            uuid: The uuid of the device for which to add the features to the database
        """
        sila_device = self.get_device_instance(uuid)

        sila_device.connect()
        features = self.get_features(uuid)
        with self.conn as conn:
            with conn.cursor() as cursor:
                for feature in features:
                    dynamic_feature = sila_device.getClient()._features[
                        feature.identifier + '\n']
                    cursor.execute(
                        'insert into features_for_data_handler values (default,%s,%s,%s,%s,%s,%s,%s) returning id',
                        [
                            feature.identifier, feature.name,
                            feature.description, feature.feature_version,
                            feature.feature_version_major,
                            feature.feature_version_minor,
                            str(uuid)
                        ])
                    feature_id = cursor.fetchone()[0]
                    for command in feature.commands:
                        dynamic_command = dynamic_feature.commands[
                            command.identifier]
                        cursor.execute(
                            'insert into commands_for_data_handler values (default,%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
                            'returning id',
                            [command.identifier, command.name, command.description, command.observable, INTERVAL,
                             META_INTERVAL, ACTIVATED, META, feature_id])
                        command_id = cursor.fetchone()[0]
                        for parameter in command.parameters:
                            if parameter.type != 'Void':
                                data_parameters = dynamic_command.parameters
                                parameter_index = list(
                                    data_parameters.fields.keys()).index(
                                        parameter.identifier)
                                parameter.type = list(data_parameters.paths.keys())[parameter_index].split('/', 1)[1]
                            cursor.execute(
                                'insert into parameters_for_data_handler values' \
                                '(default,%s,%s,%s,%s,%s,%s,%s,%s)',
                                [parameter.identifier, parameter.name, parameter.description, parameter.type, None,
                                 "parameter", "command", command_id])
                        for response in command.responses:
                            if response.type != 'Void':
                                data_responses = dynamic_command.responses
                                response_index = list(
                                    data_responses.fields.keys()).index(
                                        response.identifier)
                                response.type = list(data_responses.paths.keys())[response_index].split('/', 1)[1]
                            cursor.execute(
                                'insert into parameters_for_data_handler values' \
                                '(default,%s,%s,%s,%s,%s,%s,%s,%s)',
                                [response.identifier, response.name, response.description, response.type, None,
                                 "response", "command", command_id])
                        for intermediate in command.intermediates:
                            data_intermediates = dynamic_command.intermediate_responses
                            intermediate_index = list(
                                data_intermediates.fields.keys()).index(
                                    intermediate.identifier)
                            intermediate.type = list(
                                data_intermediates.paths.keys(
                                ))[intermediate_index].split('/', 1)[1]
                            cursor.execute(
                                'insert into parameters_for_data_handler values' \
                                '(default,%s,%s,%s,%s,%s,%s,%s,%s)',
                                [intermediate.identifier, intermediate.name, intermediate.description,
                                 intermediate.type, None, "intermediate", "command", command_id])
                        for defined_execution_error in command.defined_execution_errors:
                            cursor.execute(
                                'insert into defined_execution_errors values (default,%s,%s,%s)',
                                [
                                    defined_execution_error, "command",
                                    command_id
                                ])
                    for property in feature.properties:
                        dynamic_property = dynamic_feature.properties[
                            property.identifier]
                        cursor.execute(
                            'insert into properties_for_data_handler values (default,%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
                            'returning id',
                            [property.identifier, property.name, property.description, property.observable, INTERVAL,
                             META_INTERVAL, ACTIVATED, META, feature_id])
                        property_id = cursor.fetchone()[0]
                        response = property.response
                        data_responses = dynamic_property.responses
                        response_index = list(
                            data_responses.fields.keys()).index(
                                response.identifier)
                        response.type = list(
                            data_responses.paths.keys())[response_index].split(
                                '/', 1)[1]
                        cursor.execute(
                            'insert into parameters_for_data_handler values' \
                            '(default,%s,%s,%s,%s,%s,%s,%s,%s)',
                            [response.identifier, response.name, response.description, response.type, None,
                             "response", "property", property_id])
                        for defined_execution_error in property.defined_execution_errors:
                            cursor.execute(
                                'insert into defined_execution_errors values (default,%s,%s,%s)',
                                [
                                    defined_execution_error, "property",
                                    property_id
                                ])

    def get_features_for_data_handler(
            self, uuid: UUID) -> List[DeviceFeatureForDataHandler]:
        """Get the features of the device (specified by uuid) from the database
        Args:
            uuid: The uuid of the device for which to get the features from the database
        """
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select id,identifier,name,description,feature_version,feature_version_minor,feature_version_major from features_for_data_handler where device=%s',
                    [str(uuid)])
                result = cursor.fetchall()
                features = [
                    DeviceFeatureForDataHandler(id=row[0],
                                                identifier=row[1],
                                                name=row[2],
                                                description=row[3],
                                                feature_version=row[4],
                                                feature_version_minor=row[5],
                                                feature_version_major=row[6],
                                                commands=[],
                                                properties=[])
                    for row in result
                ]
                for feature in features:
                    feature.commands = self.get_commands_for_feature_for_data_handler(
                        feature.id)
                    feature.properties = self.get_properties_for_feature_for_data_handler(
                        feature.id)
                return features

    def get_commands_for_feature_for_data_handler(
            self, feature_id) -> List[DeviceCommandForDataHandler]:
        """Get the commands of the feature (specified by feature_id) from the database
        Args:
            feature_id: The id of the feature for which to get the commands from the database
        """
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select identifier,name,description,observable,id,interval,meta_interval,activated,meta from commands_for_data_handler where feature=%s',
                    [str(feature_id)])
                result = cursor.fetchall()
                commands = [
                    DeviceCommandForDataHandler(identifier=row[0],
                                                name=row[1],
                                                description=row[2],
                                                observable=row[3],
                                                parameters=[],
                                                responses=[],
                                                intermediates=[],
                                                defined_execution_errors=[],
                                                id=row[4],
                                                interval=row[5],
                                                meta_interval=row[6],
                                                activated=row[7],
                                                meta=row[8]) for row in result
                ]
                for command in commands:
                    command.parameters = self.get_parameters_for_command_for_data_handler(
                        command.id)
                    command.responses = self.get_responses_for_command_for_data_handler(
                        command.id)
                    command.intermediates = self.get_intermediates_for_command_for_data_handler(
                        command.id)
                    command.defined_execution_errors = \
                        self.get_defined_execution_errors_for_command_for_data_handler(command.id)
                return commands

    def get_parameters_for_command_for_data_handler(
            self, command_id) -> List[DeviceParameterForDataHandler]:
        """Get the parameters of the command (specified by command_id) from the database
        Args:
            command_id: The id of the command for which to get the parameters from the database
        """
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select type,identifier,name,description,id,value from parameters_for_data_handler where used_as=%s and parent_type=%s and parent=%s',
                    ['parameter', 'command',
                     str(command_id)])
                result = cursor.fetchall()
                parameters = [
                    DeviceParameterForDataHandler(type=row[0],
                                                  identifier=row[1],
                                                  name=row[2],
                                                  description=row[3],
                                                  id=row[4],
                                                  value=row[5])
                    for row in result
                ]
                return parameters

    def get_responses_for_command_for_data_handler(
            self, command_id) -> List[DeviceParameterForDataHandler]:
        """Get the responses of the command (specified by command_id) from the database
        Args:
            command_id: The id of the command for which to get the responses from the database
        """
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select type,identifier,name,description,id,value from parameters_for_data_handler where used_as=%s and parent_type=%s and parent=%s',
                    ['response', 'command',
                     str(command_id)])
                result = cursor.fetchall()
                responses = [
                    DeviceParameterForDataHandler(type=row[0],
                                                  identifier=row[1],
                                                  name=row[2],
                                                  description=row[3],
                                                  id=row[4],
                                                  value=row[5])
                    for row in result
                ]
                return responses

    def get_intermediates_for_command_for_data_handler(
            self, command_id) -> List[DeviceParameterForDataHandler]:
        """Get the intermediates of the command (specified by command_id) from the database
        Args:
            command_id: The id of the command for which to get the intermediates from the database
        """
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select type,identifier,name,description,id,value from parameters_for_data_handler where used_as=%s and parent_type=%s and parent=%s',
                    ['intermediate', 'command',
                     str(command_id)])
                result = cursor.fetchall()
                intermediates = [
                    DeviceParameterForDataHandler(type=row[0],
                                                  identifier=row[1],
                                                  name=row[2],
                                                  description=row[3],
                                                  id=row[4],
                                                  value=row[5])
                    for row in result
                ]
                return intermediates

    def get_defined_execution_errors_for_command_for_data_handler(
            self, command_id) -> List[str]:
        """Get the defined execution errors of the command (specified by command_id) from the database
        Args:
            command_id: The id of the command for which to get the defined execution errors from the database
        """
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select defined_execution_error from defined_execution_errors where parent_type=%s and parent=%s',
                    ['command', str(command_id)])
                result = cursor.fetchall()
                defined_execution_errors = [row[0] for row in result]
                return defined_execution_errors

    def get_properties_for_feature_for_data_handler(
            self, feature_id) -> List[DevicePropertyForDataHandler]:
        """Get the properties of the feature (specified by feature_id) from the database
        Args:
            feature_id: The id of the feature for which to get the properties from the database
        """
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select id,identifier,name,description,observable,interval,meta_interval,activated,meta from properties_for_data_handler where feature=%s',
                    [str(feature_id)])
                result = cursor.fetchall()
                properties = [
                    DevicePropertyForDataHandler(id=row[0],
                                                 identifier=row[1],
                                                 name=row[2],
                                                 description=row[3],
                                                 observable=row[4],
                                                 response=None,
                                                 defined_execution_errors=[],
                                                 interval=row[5],
                                                 meta_interval=row[6],
                                                 activated=row[7],
                                                 meta=row[8]) for row in result
                ]
                for property in properties:
                    property.response = self.get_response_for_property_for_data_handler(
                        property.id)
                    property.defined_execution_errors = \
                        self.get_defined_execution_errors_for_property_for_data_handler(property.id)
                return properties

    def get_response_for_property_for_data_handler(
            self, property_id) -> DeviceParameterForDataHandler:
        """Get the response of the property (specified by property_id) from the database
        Args:
            property_id: The id of the property for which to get the response from the database
        """
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select type,identifier,name,description,id,value from parameters_for_data_handler where used_as=%s and parent_type=%s and parent=%s',
                    ['response', 'property',
                     str(property_id)])
                row = cursor.fetchone()
                response = DeviceParameterForDataHandler(type=row[0],
                                                         identifier=row[1],
                                                         name=row[2],
                                                         description=row[3],
                                                         id=row[4],
                                                         value=row[5])
                return response

    def get_defined_execution_errors_for_property_for_data_handler(
            self, property_id) -> List[str]:
        """Get the defined execution errors of the property (specified by property_id) from the database
        Args:
            property_id: The id of the property for which to get the defined execution errors from the database
        """
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select defined_execution_error from defined_execution_errors where parent_type=%s and parent=%s',
                    ['property', str(property_id)])
                result = cursor.fetchall()
                defined_execution_errors = [row[0] for row in result]
                return defined_execution_errors

    def add_database(self, name: str, address: str, port: int):
        """Add a new database to the database
        Args:
            name: The name of the new database that should be added to the database
            address: The IP address of the new database that should be added to the database
            port: The port of the new database that should be added to the database
        """
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'insert into databases values (default,%s,%s,%s)',
                    [name, address, port])

    def discover_sila_devices(self):
        """Triggers the sila autodiscovery
        Returns:
            The list of discovered devices
        """
        return find()

    def get_log(self,
                from_date: int = 0,
                to_date: int = datetime.now().timestamp(),
                exclude=None):
        """Get log entries from database
        Args:
            start (datetime): The first date
            end (datetime): The last date
            exclude: A dictionary containing the log levels that
            should be excluded
        Returns:
            Log entries
        """
        exclude_string = ''

        if exclude is not None:
            if exclude['info']:
                exclude_string += f'type != {LogLevel.INFO} '
            if exclude['warning']:
                seperator = 'and ' if exclude['info'] else ''
                exclude_string += seperator + f'type != {LogLevel.WARNING} '
            if exclude['critical']:
                seperator = 'and ' if exclude['info'] or exclude[
                    'warning'] else ''
                exclude_string += seperator + f'type != {LogLevel.CRITICAL} '
            if exclude['error']:
                seperator = 'and ' if exclude['info'] or exclude[
                    'warning'] or exclude['critical'] else ''
                exclude_string += seperator + f'type != {LogLevel.ERROR} '

            exclude_string += 'and ' if exclude['info'] or exclude[
                'warning'] or exclude['critical'] or exclude['error'] else ''
            print(exclude_string)

        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'select type,device,time,message from log '\
                f'where '\
                f'{exclude_string} '\
                f'time>=%s and time<=%s order by time desc',
                [from_date, to_date])
                return [{
                    'type': row[0],
                    'device': row[1],
                    'time': row[2],
                    'message': row[3]
                } for row in cursor]

    def get_booking_entry(self, id: int):
        return get_booking_entry(id)

    def get_device_bookings(self, device: UUID, start: int,
                            stop: int) -> List[BookingInfo]:
        return get_device_booking_info(device, start, stop)

    def get_all_bookings(self, start: int, stop: int) -> List[BookingInfo]:
        return get_booking_info(start, stop)

    def get_device_bookings_with_name(self, device: UUID, start: int,
                                      stop: int) -> List[BookingInfoWithNames]:
        return get_device_booking_info_with_names(device, start, stop)

    def get_all_bookings_with_name(self, start: int,
                                   stop: int) -> List[BookingInfoWithNames]:
        return get_booking_info_with_names(start, stop)

    def book_device(self, name: str, user: int, device: UUID, start: int,
                    stop: int) -> int:
        return book(BookingInfo(-1, name, start, stop, user, device))

    def delete_booking_entry(self, id: int):
        if id_is_valid(id):
            delete_booking_entry(id)

    def get_all_experiments(self) -> experiment.Experiment:
        return experiment.get_all_experiments()

    def get_user_experiments(self, user: int) -> experiment.Experiment:
        return experiment.get_user_experiments(user)

    def create_experiment(self, name: str, start: int, end: int, user: int,
                          devices: List[UUID], script: int) -> int:
        return experiment.create_experiment(name, start, end, user, devices,
                                            script)

    def delete_experiment(self, experimentID: int):
        return experiment.delete_experiment(experimentID)

    def get_user_scripts(self, user: int) -> List[script.Script]:
        return script.get_user_scripts(user)

    def get_user_scripts_info(self, user: int) -> List[script.ScriptInfo]:
        return script.get_user_scripts_info(user)

    def get_user_script(self, script_id: int) -> script.Script:
        return script.get_user_script(script_id)

    def get_user_script_info(self, script_id: int) -> script.ScriptInfo:
        return script.get_user_script_info(script_id)

    def create_user_script(self, name: str, fileName: str, user: int,
                           data: str) -> int:
        return script.create_user_script(name, fileName, user, data)

    def delete_user_script(self, script_id: int):
        script.delete_user_script(script_id)

    def set_user_script_info(self, script_id: int, name: str, file_name: str,
                             user_id: int):
        script.set_user_script_info(script_id, name, file_name, user_id)

    def set_user_script(self, script_id: int, name: str, file_name: str,
                        user_id: int, data: str):
        script.set_user_script(script_id, name, file_name, user_id, data)
