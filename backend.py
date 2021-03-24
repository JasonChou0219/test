"""
:PROJECT: SiLA2_device_manager

:details: The API of the backend.

:file:    backend.py
:authors: Lukas Bromig, David Leiter, Alexandru Mardale

:date: (creation)          2021-01-27
:date: (last modification) 2021-01-27

**Copyright**:
This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

For further Information see LICENSE file that comes with this distribution.
"""

from fastapi import FastAPI, Body, Depends, HTTPException, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from logging import error
import traceback
import sys
import aioredis
import json
import msgpack
import configparser
import base64
from source.device_manager.database import get_redis_pool
from source.device_manager.data_directories import DATA_DIRECTORY

from source.backend.device_manager_service import DeviceManagerService, DeviceInfoModel, NewDeviceModel, BookingModel, \
    ExperimentBookingModel, ScriptInfoModel, ScriptModel, DeviceCommandParameters, \
    NewDatabaseModel, DatabaseInfoModel, DeviceCommandParameter
import source.device_manager.user as user
from source.device_manager.experiment import get_experiment_user, start_experiment, stop_experiment, receive_experiment_status


class Status(BaseModel):
    """ Class containing the status of a running experiment"""
    running: bool


config = configparser.ConfigParser()

try:
    config.read(f'{DATA_DIRECTORY}/device-manager.conf')
except Exception:
    print("Could not read Config File!")
    exit()

app = FastAPI()


# handle uncaught exceptions
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        print(traceback.print_exc(file=sys.stdout))
        error(f'Unhandled Error: {sys.exc_info()} ')
        return Response("Internal server error", status_code=500)


app.middleware('http')(catch_exceptions_middleware)

# required during development because the frontend is typically served by a
# different server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

secret_key = base64.b64decode(config['Security']['SecretKey'])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

expiration_delta = 3600 * 12  # 12 Hours
refresh_expiration_delta = 3600 * 12 * 7  # A Week


class User(BaseModel):
    """ Contains user information for user management and user authentication """
    id: Optional[int]
    name: str
    fullName: str
    role: str
    newPassword: Optional[str]
    oldPassword: Optional[str]


class ResetPasswordData(BaseModel):
    """ Required for resetting of passwords """
    newPassword: str
    oldPassword: Optional[str]


class LoginCredentials(BaseModel):
    """ Required for user authentication during login """
    username: str
    password: str


def create_token(username: str, expiration: int):
    """
    Creates an authentication token for the current user

    :param username: The name of the current user
    :type username: str
    :param expiration: Expiration date of the user token
    :type expiration: int
    :return: Returns username, expiration date, secret key and JWT algorithm
    :rtype: dict
    """
    return jwt.encode({
        'sub': username,
        'exp': expiration,
    }, secret_key, 'HS256')


def decode_token(token: str = Depends(oauth2_scheme)):
    """
    Decodes and verifies token using the JWT algorithm HS256

    :param token: The user token
    :type token: str
    :return: user key/ payload
    :rtype: str
    """
    payload = jwt.decode(token, secret_key, algorithms='HS256')
    return payload.get('sub')


@app.post('/api/login')
def login(form: OAuth2PasswordRequestForm = Depends()):
    """
    Transfer authentication details for Auth2 authentication. Compare authentication data with registered users.
    Create access token and assign expiration date.

    :param form: A form containing the necessary authentication details
    :type form: OAuth2PasswordRequestForm
    :return: A dictionary of authentication elements such as tokens and expiration date
    :rtype: dict
    """
    if not user.authenticate(form.username, form.password):
        raise HTTPException(401, 'Could not authenticate')

    expiration_date = int(datetime.utcnow().timestamp()) + expiration_delta
    refresh_expiration_date = int(
        datetime.now().timestamp()) + refresh_expiration_delta
    access_token = create_token(form.username, expiration_date)
    refresh_token = create_token(form.username, refresh_expiration_date)
    role = user.get_user_by_name(form.username).role
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
        'expiration': expiration_date,
        'role': role
    }


@app.get('/api')
def root(username: str = Depends(decode_token)):
    return 'Nothing to see here!'


@app.get('/api/users')
def get_users(username: str = Depends(decode_token)):
    if user.is_admin(username):
        users = user.get_users()
        return [
            User(id=user.id,
                 name=user.name,
                 fullName=user.fullName,
                 role=user.role) for user in users
        ]


@app.get('/api/users/me')
def get_current_user(username: str = Depends(decode_token)):
    """
    Fetches the details of the current user.

    :param username: The name of the current user
    :type: str
    :return: An object containing information on the current user
    :rtype: User
    """
    current_user = user.get_user_by_name(username)
    return User(id=current_user.id,
                name=current_user.name,
                fullName=current_user.fullName,
                role=current_user.role)


@app.post('/api/users')
def add_user(new_user: User, username: str = Depends(decode_token)):
    """
    Saves a new user to the postgreSQL database

    :param new_user: Information of the new user
    :type new_user: User
    :param username: The name of hte executing user
    :type username: str
    :return: None
    """
    if user.is_admin(username):
        try:
            user.add_user(new_user.name, new_user.fullName,
                          new_user.newPassword, new_user.role)
        except user.UserExistsError as e:
            raise HTTPException(
                403, 'Can not create User. The name is already taken.') from e
    return


@app.put('/api/users/{id}')
def update_user(id: int, new_user: User,
                username: str = Depends(decode_token)):
    """
    Updates the stored information of an existing user. Can be used to change the user role or name.

    :param id: Internally assigned user id
    :type id: int
    :param new_user: The updated user information
    :type new_user: User
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    if user.is_admin(username):
        user.update_user(id, new_user.name, new_user.fullName,
                         new_user.newPassword, new_user.role)
    return


@app.put('/api/users/{id}/password')
def reset_password(id: int,
                   password_data: ResetPasswordData,
                   username: str = Depends(decode_token)):
    """
    Changes the password of the user to a new one.

    :param id: Internally assigned user id
    :type id: int
    :param password_data: Contains the old and the new password
    :type password_data: ResetPasswordData
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    print(password_data.newPassword)
    if user.is_admin(username):
        user.set_password(id, password_data.newPassword)
    else:
        if (password_data.oldPassword is None) or (user.authenticate(
                password_data.oldPassword) is False):
            raise HTTPException(403, "Can't reset passwort")
        user.set_password(id, password_data.newPassword)


@app.delete('/api/users/{id}')
def delete_user(id: int, username: str = Depends(decode_token)):
    """
    Delete a user from the postgreSQL

    :param id: Internally assigned user id
    :type id: int
    :param username: The name of the executing user
    :type username: int
    :return: None
    """
    if user.is_admin(username):
        user.delete_user(id)
    return


@app.get('/api/users/{id}')
def get_user(id: int, username: str = Depends(decode_token)):
    """
    Fetches detailed information of a user from the postgreSQL database

    :param id: Internally assigned user id
    :type id: int
    :param username: The name of the executing user
    :type username: int
    :return: An object containing the user information
    :rtype: User
    """
    if user.is_admin(username):
        u = user.get_user(id)
        return User(id=u.id, name=u.name, fullName=u.fullName, role=u.role)


@app.get('/api/devices')
def get_devices(username: str = Depends(decode_token)):
    device_manager_service = DeviceManagerService()
    return {'data': device_manager_service.get_devices()}


@app.post('/api/devices')
def add_device(device: NewDeviceModel, username: str = Depends(decode_token)):
    """
    Addition of a new device to the postgreSQL database

    :param device: Device information object including name, type, address, port etc. etc. but without an assigned internal UUID4
    :type device: NewDeviceModel
    :param username: The name of the executing user
    :type username: int
    :return: None
    """
    device_manager_service = DeviceManagerService()
    device_manager_service.add_device(device)
    return


@app.get('/api/devices/{uuid}')
def get_device(uuid: str, username: str = Depends(decode_token)):
    """
    Get device information for a provided device-uuid

    :param uuid: Unique identifier (UUID4) of the device used for internal reference
    :type uuid: str
    :param username:
    :type username: str
    :return: Device information including name, type, address, port etc. etc.
    :rtype: DeviceInfo
    """
    device_manager_service = DeviceManagerService()
    return device_manager_service.get_device(uuid)


@app.put('/api/devices/{uuid}')
def set_device(uuid: str,
               device: DeviceInfoModel,
               username: str = Depends(decode_token)):
    """

    :param uuid: Internally assigned device uuid
    :type uuid: str
    :param device: A device information object
    :type device: DeviceInfoModel
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    device_manager_service.set_device(uuid, device)
    return


@app.delete('/api/devices/{uuid}')
def delete_device(uuid: str, username: str = Depends(decode_token)):
    """
    Delete the device from postgreSQL database and delete generated dynamic client files in temporary data

    :param uuid: Internally assigned device uuid
    :type uuid: str
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    device_manager_service.delete_device(uuid)
    return


@app.get('/api/deviceStatus/{uuid}')
def device_status(uuid: str, username: str = Depends(decode_token)):
    """
    Get the availability status of the device by pinging the device server and retrieving the booking information

    :param uuid: Internally assigned device uuid
    :type uuid: str
    :param username: The name of the executing user
    :type username: str
    :return: An object containing status information
    :rtype: DeviceStatus
    """
    device_manager_service = DeviceManagerService()
    return device_manager_service.get_status(uuid)


@app.get('/api/deviceFeatures/{uuid}')
def device_features(uuid: str, username: str = Depends(decode_token)):
    """
    Get all features and associated information of the requested device.

    :param uuid: Internally assigned device uuid
    :type uuid: str
    :param username: The name of the executing user
    :type username: str
    :return: List of SiLA feature objects that include all associated information
    """
    device_manager_service = DeviceManagerService()
    return {'data': device_manager_service.get_features(uuid)}


@app.get('/api/deviceFeaturesDataHandler/{uuid}')
def device_features_for_datahandler(uuid: str, username: str = Depends(decode_token)):
    """
    Get all features and associated information of the requested device.

    :param uuid: Internally assigned device uuid
    :type uuid: str
    :param username: The name of the executing user
    :type username: str
    :return: List of SiLA feature objects that include all associated information
    """
    device_manager_service = DeviceManagerService()
    return {'data': device_manager_service.get_features_for_data_handler(uuid)}

@app.post('/api/device/{uuid}/qualifiedFeatureIdentifier/{feature_originator}/{feature_category}/{feature_identifier}/v{feature_version_major}/command/{command_id}')
def call_feature_command(uuid: str,
                         feature_originator: str,
                         feature_category: str,
                         feature_identifier: str,
                         feature_version_major: str,
                         command_id: str,
                         parameterList: DeviceCommandParameters,
                         username: str = Depends(decode_token)):
    """
    Executes the specified command and returns the response

    :param uuid: Internally assigned device uuid
    :type uuid: str
    :param feature_originator: The SiLA 2 Originator of the feature the command belongs to
    :type feature_originator: str
    :param feature_category: The SiLA 2 Category of the feature the command belongs to
    :type feature_category: str
    :param feature_identifier: The SiLA 2 Feature Identifier of the feature the command belongs to
    :type feature_identifier: str
    :param feature_version_major: The SiLA 2 Major Feature Version of the feature the command belongs to
    :type feature_version_major: str
    :param command_id: the id of the command to be called
    :type command_id: str
    :param parameterList: A list of parameters required by the command
    :type parameterList: DeviceCommandParameters
    :param username: The name of the executing user
    :type username: str
    :return: The response of the call
    """
    qualified_feature_identifier = feature_originator + '/' + feature_category + '/' + feature_identifier + '/v' + \
                                   feature_version_major
    device_manager_service = DeviceManagerService()
    return device_manager_service.call_feature_command(uuid, qualified_feature_identifier,
                                                       command_id,
                                                       parameterList.params)

@app.get('/api/device/{uuid}/qualifiedFeatureIdentifier/{feature_originator}/{feature_category}/{feature_identifier}/v'
         '{feature_version_major}/property/{property_id}')
def get_feature_property(uuid: str,
                         feature_originator: str,
                         feature_category: str,
                         feature_identifier: str,
                         feature_version_major: str,
                         property_id: str,
                         username: str = Depends(decode_token)):
    """
    Requests the specified property and returns the response

    :param uuid: Internally assigned device uuid
    :type uuid: str
    :param feature_originator: The SiLA 2 Originator of the feature the property belongs to
    :type feature_originator: str
    :param feature_category: The SiLA 2 Category of the feature the property belongs to
    :type feature_category: str
    :param feature_identifier: The SiLA 2 Feature Identifier of the feature the property belongs to
    :type feature_identifier: str
    :param feature_version_major: The SiLA 2 Major Feature Version of the feature the property belongs to
    :type feature_version_major: str
    :param property_id: The id of the property
    :type property_id: str
    :param username: The name of the executing user
    :type username: str
    :return: The response of the call
    """
    qualified_feature_identifier = feature_originator + '/' + feature_category + '/' + feature_identifier + '/v' + \
                                   feature_version_major
    device_manager_service = DeviceManagerService()
    return device_manager_service.get_feature_property(uuid, qualified_feature_identifier,
                                                       property_id)


@app.get('/api/databases')
def get_databases(username: str = Depends(decode_token)):
    """
    Retrieves all information on the registered databases

    :param username: The name of the executing user
    :type username: str
    :return: Returns a list of objects containing database information
    :rtype: List[DatabaseInfo]
    """
    device_manager_service = DeviceManagerService()
    return {'data': device_manager_service.get_databases()}


@app.post('/api/databases')
def add_database(database: NewDatabaseModel, username: str = Depends(decode_token)):
    """
    Add a new database to the system. The database information is stored in the postgreSQL database.

    :param database: An object containing the information of the new database, i.e. connection details and name.
    :type database: NewDatabaseModel
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    device_manager_service.add_database(database)
    return


@app.get('/api/databases/{id}')
def get_database(id: int, username: str = Depends(decode_token)):
    """
    Get information on a specific database

    :param id: Internally assigned id of the database
    :type id: int
    :param username: The name of the executing user
    :type username: str
    :return: An object containing information on the database
    :rtype: DatabaseInfo
    """
    device_manager_service = DeviceManagerService()
    return device_manager_service.get_database(id)

@app.get('/api/databaseStatus/{id}')
def database_status(id: int, username: str = Depends(decode_token)):
    """
    Check the connection status of the database by pinging the database server

    :param id: Internally assigned id of the database
    :type id: int
    :param username: The name of the executing user
    :type username: str
    :return: An object containing the status information
    :rtype: DatabaseStatus
    """
    device_manager_service = DeviceManagerService()
    return device_manager_service.get_database_status(id)

@app.put('/api/databases/{id}')
def set_database(id: int,
                 database: DatabaseInfoModel,
                 username: str = Depends(decode_token)):
    """


    :param id: Internally assigned id of the database
    :type id: int
    :param database: An object containing database information
    :type database: DatabaseInfoModel
    :param username: The name of the executing user
    :type username: str
    :return:
    """
    device_manager_service = DeviceManagerService()
    device_manager_service.set_database(id, database)
    return


# TODO: Unlink device from database when database is deleted
@app.delete('/api/databases/{id}')
def delete_database(id: int, username: str = Depends(decode_token)):
    """
    Delete a registered database from the postgreSQL database

    :param id: Internally assigned database id
    :type id: int
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    device_manager_service.delete_database(id)
    return


@app.put('/api/devices/{uuid}/database')
def link_database(uuid: str, id: int = Body(...), username: str = Depends(decode_token)):
    """
    Link a database to a device. Required for the data-handler functionality.

    :param uuid: Internally assigned device-uuid (uuid4)
    :type uuid: str
    :param id: Internally assigned database id
    :type id: int
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    device_manager_service.link_database(uuid, id)
    return


@app.delete('/api/devices/{uuid}/database')
def unlink_database(uuid: str, username: str = Depends(decode_token)):
    """
    Unlink a database from a device. The link is deleted.

    :param uuid: Internally assigned device-uuid (uuid4)
    :type uuid: str
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    device_manager_service.unlink_database(uuid)
    return


@app.put('/api/devices/{uuid}/dataHandler')
def set_device_attributes_for_data_handler(uuid: str,
                                           active: bool = Body(...),
                                           username: str = Depends(decode_token)):
    """
    Sets the available attribute of the device status to the specified state.

    :param uuid: Internally assigned device-uuid
    :type uuid: str
    :param active: The new state setting of the device
    :type active: bool
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    device_manager_service.set_device_attributes_for_data_handler(uuid, active)
    return


@app.put('/api/devices/{uuid}/features/{feature_id}/dataHandler')
def set_feature_attributes_for_data_handler(uuid: str,
                                            feature_id: str,
                                            active: bool = Body(...),
                                            meta: bool = Body(...),
                                            username: str = Depends(decode_token)):
    """
    Set the state of the data acquisition mode on a feature level. De/Activate data acquisition and switch from meta to
    non-meta polling interval.

    :param uuid: Internally assigned device-uuid
    :type uuid: str
    :param feature_id: The SiLA id of the feature
    :type feature_id: str
    :param active: The state of the data-handler data acquisition mode of this feature of the device. To be set!
    :type active: bool
    :param meta: The kind of polling interval that shall be used. To be set! Defaults to meta (True).
    :type meta: bool
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    device_manager_service.set_feature_attributes_for_data_handler(uuid, feature_id, active, meta)
    return


@app.put('/api/devices/{uuid}/features/{feature_id}/commands/{command_id}/dataHandler')
def set_command_attributes_for_data_handler(uuid: str,
                                            feature_id: str,
                                            command_id: str,
                                            parameters: List[DeviceCommandParameter],
                                            active: bool = Body(...),
                                            meta: bool = Body(...),
                                            nonMetaInterval: int = Body(default=None),
                                            metaInterval: int = Body(default=None),
                                            username: str = Depends(decode_token)):
    """
    Set the state of the data acquisition mode on a command level. De/Activate data acquisition and switch from meta to
    non-meta polling interval.

    :param uuid: Internally assigned device-uuid
    :type uuid: str
    :param feature_id: The SiLA id of the feature the command belongs to
    :type feature_id: str
    :param command_id: The SiLA id of the command
    :type command_id: str
    :param parameters: The parameter to be used by the data-handler
    :type parameters: List[DeviceCommandParameter]
    :param active: The state of the data-handler data acquisition mode this command of the device. To be set!
    :type active: bool
    :param meta: The kind of polling interval that shall be used. To be set! Defaults to meta (True).
    :type meta: bool
    :param nonMetaInterval: Polling interval for non-meta data acquisition
    :type nonMetaInterval: int
    :param metaInterval: Polling interval for meta data acquisition
    :type metaInterval: int
    :param username: The name of the executing user
    :type username: str
    :return: None
    :return:
    """
    device_manager_service = DeviceManagerService()
    device_manager_service.set_command_attributes_for_data_handler(uuid, feature_id, command_id, active, meta,
                                                                   nonMetaInterval, metaInterval, parameters)
    return


@app.put('/api/devices/{uuid}/features/{feature_id}/properties/{property_id}/dataHandler')
def set_property_attributes_for_data_handler(uuid: str,
                                             feature_id: str,
                                             property_id: str,
                                             active: bool = Body(...),
                                             meta: bool = Body(...),
                                             nonMetaInterval: int = Body(default=None),
                                             metaInterval: int = Body(default=None),
                                             username: str = Depends(decode_token)):
    """
    Set the state of the data acquisition mode on a property level. De/Activate data acquisition and switch from meta to
    non-meta polling interval.

    :param uuid: Internally assigned device-uuid
    :type uuid: str
    :param feature_id: The SiLA id of the feature the property belongs to
    :type feature_id: str
    :param property_id: The SiLA id of the property
    :type property_id: str
    :param active: The state of the data-handler data acquisition mode this property of the device. To be set!
    :type active: bool
    :param meta: The kind of polling interval that shall be used. To be set! Defaults to meta (True).
    :type meta: bool
    :param nonMetaInterval: Polling interval for non-meta data acquisition
    :type nonMetaInterval: int
    :param metaInterval: Polling interval for meta data acquisition
    :type metaInterval: int
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    device_manager_service.set_property_attributes_for_data_handler(uuid, feature_id, property_id, active, meta,
                                                                    nonMetaInterval, metaInterval)
    return


@app.get('/api/silaDiscovery/')
def sila_discovery():
    """
    Searches for all registered SiLA devices on the network and returns the information

    :return: Returns a list containing all discovered devices and the corresponding information available
    :rtype: List[List[SilaServerInfo]]
    """
    device_manager_service = DeviceManagerService()
    data = device_manager_service.discover_sila_devices()
    return {'data': device_manager_service.discover_sila_devices()}


@app.get('/api/deviceLog/')
def device_log(start: int = 0,
               end: int = datetime.now().timestamp(),
               excludeInfo: bool = False,
               excludeWarning: bool = False,
               excludeCritical: bool = False,
               excludeError: bool = False,
               username: str = Depends(decode_token)):
    """
    Get the device logs.

    :param start: Time of the first log entry to be gathered. Defaults to 0.
    :type start: int, optional
    :param end: Time of the last log entry to be gathered.  Defaults to current time.
    :type end: int, optional
    :param excludeInfo: Filter Info log level messages
    :type excludeInfo: bool, optional
    :param excludeWarning: Filter Warning log level messages
    :type excludeWarning: bool, optional
    :param excludeCritical: Filter Critical log level messages
    :type excludeCritical: bool, optional
    :param excludeError: Filter Error log level messages
    :type excludeError: bool, optional
    :param username: The name of the executing user
    :type username: str
    :return: A dictionary containing the requested log messages
    :rtype: dict
    """
    device_manager_service = DeviceManagerService()
    return {
        'data':
        device_manager_service.get_log(
            start, end, {
                'info': excludeInfo,
                'warning': excludeWarning,
                'critical': excludeCritical,
                'error': excludeError
            })
    }


@app.get('/api/bookings')
def get_booking_list(start: int = 0,
                     end: int = 2**32 - 1,
                     username: str = Depends(decode_token)):
    """
    Fetches the registered bookings from the postgreSQL database

    :param start: The time of the first booking to be gathered. Defaults to 0.
    :type start: int, optional
    :param end: The time of the last booking to be gathered.
    :type end: int, optional
    :param username: The name of the executing user
    :type username: str
    :return: A list of all bookings
    :rtype: List[booking_info]
    """
    device_manager_service = DeviceManagerService()
    return {'data': device_manager_service.get_bookings(start, end)}


@app.post('/api/bookings')
def book_device(bookingInfo: BookingModel,
                username: str = Depends(decode_token)):
    """
    Store a booking for a device in the postgreSQL database

    :param bookingInfo: The booking information
    :type bookingInfo: BookingModel
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    device_manager_service.book_device(bookingInfo.name, bookingInfo.user,
                                       bookingInfo.device, bookingInfo.start,
                                       bookingInfo.end)
    return


@app.get('/api/bookings/device/{uuid}')
def get_device_booking_list(uuid: str,
                            start: int = 0,
                            end: int = datetime.now().timestamp(),
                            username: str = Depends(decode_token)):
    """
    Fetches a list of device bookings

    :param uuid: Internally assigned device uuid
    :type uuid: str
    :param start: The time of the first booking entry to be gathered. Defaults to 0.
    :type start: int, optional
    :param end: The time of the last booking entry to be gathered. Defaults to current time.
    :type end: int, optional
    :param username: The name of the executing user
    :type username: str
    :return: List of booking information objects for the device
    :rtype: List[BookingInfoWithNames]
    """
    device_manager_service = DeviceManagerService()
    return {
        'data': device_manager_service.get_device_bookings(uuid, start, end)
    }


@app.get('/api/bookings/{bookingID}')  #, methods=['GET', 'DELETE'])
def get_booking(bookingID: int, username: str = Depends(decode_token)):
    """
    Get booking information for a booking id

    :param bookingID: The id of the requested booking
    :type bookingID: int
    :param username: The name of the executing user
    :type username: str
    :return: Information of the booking
    :rtype: BookingInfo
    """
    device_manager_service = DeviceManagerService()
    return {'data': device_manager_service.get_booking_entry(bookingID)}


@app.delete('/api/bookings/{bookingID}')  #, methods=['GET', 'DELETE'])
def delete_booking(bookingID: int, username: str = Depends(decode_token)):
    """
    Delete a booking from the  postgreSQL by id

    :param bookingID: The booking id
    :type bookingID: int
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    current_user = user.get_user_by_name(username)
    device_manager_service = DeviceManagerService()
    booking_entry = device_manager_service.get_booking_entry(bookingID)
    if (booking_entry.user != current_user.id) and (current_user.role !=
                                                    'admin'):
        raise HTTPException(
            403,
            "Can't delete the booking entry. Only the owning user or an administrator can delete a booking entry"
        )
    device_manager_service.delete_booking_entry(bookingID)
    return


@app.get('/api/experiments')
def get_experiments(username: str = Depends(decode_token)):
    """
    Get information of all stored experiments

    :param username: The name of the executing user
    :type username: str
    :return: Returns a list of experiments with the corresponding information
    :rtype: List[Experiment]
    """
    device_manager_service = DeviceManagerService()
    return {'data': device_manager_service.get_all_experiments()}


@app.post('/api/experiments')
def create_experiment(experiment: ExperimentBookingModel,
                      username: str = Depends(decode_token)):
    """
    Store a new experiment in the postgreSQL database

    :param experiment: The new experiment
    :type experiment: ExperimentBookingModel
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    userID = user.get_user_by_name(username).id
    device_manager_service = DeviceManagerService()
    device_manager_service.create_experiment(experiment.name, experiment.start,
                                             experiment.end, userID,
                                             experiment.devices,
                                             experiment.scriptID)
    return


@app.put('/api/experiments/edit/{experimentID}')
def edit_experiment(experimentID: int,
                    experiment: ExperimentBookingModel,
                    username: str = Depends(decode_token)):
    """
    Edit an already existing experiment

    :param experimentID: The internal experiment id
    :type experimentID: int
    :param experiment: The experiment information object
    :type experiment: ExperimentBookingModel
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    print(f'experiment data {experiment}')
    userID = user.get_user_by_name(username).id
    device_manager_service = DeviceManagerService()
    device_manager_service.edit_experiment(experimentID, experiment.name,
                                           experiment.start,
                                           experiment.end, userID,
                                           experiment.devices,
                                           experiment.scriptID)
    return


@app.delete('/api/experiments/{experimentID}')
def delete_experiment(experimentID: int,
                      username: str = Depends(decode_token)):
    """
    Delete an experiment from the postgreSQL database.

    :param experimentID: The internal id of the experiment to be deleted
    :type experimentID: str
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    current_user = user.get_user_by_name(username)
    device_manager_service = DeviceManagerService()
    if (get_experiment_user(experimentID) !=
            current_user.id) and (current_user.role != 'admin'):
        raise HTTPException(
            403,
            "Can't delete the experiment. Only the owning user or an administrator can delete an experiment"
        )
    device_manager_service.delete_experiment(experimentID)
    return


@app.get('/api/scripts')
def get_user_scripts_info(username: str = Depends(decode_token)):
    """
    Get the information of all registered user-scripts

    :param username: The name of the executing user
    :type username: str
    :return: A list of script objects that contain the script content and information
    :rtype: List[Script]
    """
    device_manager_service = DeviceManagerService()
    current_user = user.get_user_by_name(username)
    return {
        'data': device_manager_service.get_user_scripts_info(current_user.id)
    }


@app.get('/api/scripts/{scriptID}')
def get_user_script(scriptID: int, username: str = Depends(decode_token)):
    """
    Get the information of a specific user-scripts

    :param scriptID: The internally assigned script id
    :type scriptID: int
    :param username: The name of the executing user
    :type username: str
    :return: The script object containing the scripts content and information
    :rtype: Script
    """
    device_manager_service = DeviceManagerService()
    current_user = user.get_user_by_name(username)
    script_info = device_manager_service.get_user_script_info(scriptID)
    if (script_info.user != current_user.id) and (current_user.role !=
                                                  'admin'):
        raise HTTPException(
            403,
            "Can't get the script. Only the owning user or an administrator can get a script"
        )
    return device_manager_service.get_user_script(scriptID)


@app.post('/api/scripts')
def upload_user_script(script: ScriptModel,
                       username: str = Depends(decode_token)):
    """
    Add a new script object to the postgreSQL database

    :param script: The script object containing content and additional information
    :type script: ScriptModel
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    current_user = user.get_user_by_name(username)
    device_manager_service.create_user_script(script.name, script.fileName,
                                              current_user.id, script.data)
    return


@app.delete('/api/scripts/{scriptID}')
def delete_user_script(scriptID: int, username: str = Depends(decode_token)):
    """
    Delete a specific user-script from the postgreSQL database

    :param scriptID: The id of the script
    :type scriptID: str
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    current_user = user.get_user_by_name(username)
    script_info = device_manager_service.get_user_script_info(scriptID)
    if (script_info.user != current_user.id) and (current_user.role !=
                                                  'admin'):
        raise HTTPException(
            403,
            "Can't delete the script. Only the owning user or an administrator can delete a script"
        )

    device_manager_service.delete_user_script(scriptID)
    return


@app.put('/api/scripts/{scriptID}/info')
def set_user_script_info(scriptID: int,
                         info: ScriptInfoModel,
                         username: str = Depends(decode_token)):
    """


    :param scriptID: The id of the script
    :type scriptID: int
    :param info: The object containing information and content of the script
    :type info: ScriptInfoModel
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    current_user = user.get_user_by_name(username)
    script_info = device_manager_service.get_user_script_info(scriptID)
    if (script_info.user != current_user.id) and (current_user.role !=
                                                  'admin'):
        raise HTTPException(
            403,
            "Can't modify the script. Only the owning user or an administrator can modify a script"
        )

    device_manager_service.set_user_script_info(scriptID, info.name,
                                                info.fileName, current_user.id)
    return


@app.put('/api/scripts/{scriptID}/')
def set_user_script(scriptID: int,
                    script: ScriptModel,
                    username: str = Depends(decode_token)):
    """


    :param scriptID: The id of the script

    :type scriptID: int
    :param script: The object containing the script content and information
    :type script: ScriptModel
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    device_manager_service = DeviceManagerService()
    current_user = user.get_user_by_name(username)
    script_info = device_manager_service.get_user_script_info(scriptID)
    if (script_info.user != current_user.id) and (current_user.role !=
                                                  'admin'):
        raise HTTPException(
            403,
            "Can't modify the script. Only the owning user or an administrator can modify a script"
        )

    device_manager_service.set_user_script(scriptID, script.name,
                                           script.fileName, current_user.id,
                                           script.data)
    return


@app.put('/api/experiments/{experimentID}/status')
async def control_experiment(status: Status,
                         experimentID: int,
                         username: str = Depends(decode_token)):
    """
    Asynchronous function to keep track of the experiment status. Updates the experiment status in the databse.

    :param status: The status whether the experiment is running or not
    :type status: bool
    :param experimentID: The id of the experiment
    :type experimentID: int
    :param username: The name of the executing user
    :type username: str
    :return: None
    """
    if status.running:
        await start_experiment(experimentID)
    else:
        await stop_experiment(experimentID)
    return


# Todo allow authentication !
@app.websocket("/ws/experiments_status")
async def experiment_status_websocket(
        websocket: WebSocket):  # , username:str = Depends(decode_token)):
    """
    Asynchronous function that forwards the experiment status via websocket

    :param websocket: The websocket the information is transferred by
    :type websocket: Websocket
    :return: None
    """
    pool = await get_redis_pool()
    channels = await pool.subscribe('experiment_status')
    await websocket.accept()
    print("Websocket status connect")
    try:
        while await channels[0].wait_message():
            message = msgpack.unpackb(await channels[0].get(), raw=False)
            await websocket.send_json(data=message)
        await websocket.close(code=1000)
    except WebSocketDisconnect:
        print("Websocket status disconnect")


# Todo allow authentication !
@app.websocket("/ws/experiments_logs")
async def experiment_logs_websocket(
        websocket: WebSocket):  # , username:str = Depends(decode_token)):
    """
    Asynchronous function that forwards the experiment logs of the docker container via websocket

    :param websocket: The websocket the information is transferred by
    :type websocket: Websocket
    :return: None
    """
    pool = await get_redis_pool()
    channels = await pool.subscribe('experiment_logs')
    await websocket.accept()
    print("Websocket logs connect")
    try:
        while await channels[0].wait_message():
            message = msgpack.unpackb(await channels[0].get(), raw=False)
            await websocket.send_json(data=message)
        await websocket.close(code=1000)
    except WebSocketDisconnect:
        print("Websocket logs disconnect")
