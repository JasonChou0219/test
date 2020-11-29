from fastapi import FastAPI, Body, Depends, HTTPException, Request, Response, WebSocket
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
import msgpack
from source.device_manager.database import get_redis_pool

from source.backend.device_manager_service import DeviceManagerService, DeviceInfoModel, NewDeviceModel, BookingModel, ExperimentBookingModel, ScriptInfoModel, ScriptModel, DeviceCommandParameters
import source.device_manager.user as user
from source.device_manager.experiment import get_experiment_user, start_experiment, stop_experiment,receive_experiment_status


class Status(BaseModel):
    running: bool


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
# must be replaced
secret_key= b'\x13\\TyF\xca\x98=\x02W\xf8,\x07K#\xbc\x8b\xcdA'\
                           b'\x05!\xf0\x1a\x05yK\xb3\x03b\x1b\xbd}1z\xc6&p'\
                           b'\xf2\xc2\x8d#~\xd0\x87@\xd8uj2Z\xf2\xb1\x14!\xe7'\
                           b'\xdc\xd0\xc6\xa3(\x9f\x8e{;'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

expiration_delta = 3600 * 12  # 12 Hours
refresh_expiration_delta = 3600 * 12 * 7  # A Week


class User(BaseModel):
    id: Optional[int]
    name: str
    fullName: str
    role: str
    newPassword: Optional[str]
    oldPassword: Optional[str]


class ResetPasswordData(BaseModel):
    newPassword: str
    oldPassword: Optional[str]


class LoginCredentials(BaseModel):
    username: str
    password: str


def create_token(username: str, expiration: int):
    return jwt.encode({
        'sub': username,
        'exp': expiration,
    }, secret_key, 'HS256')


def decode_token(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, secret_key, algorithms='HS256')
    return payload.get('sub')


@app.post('/api/login')
def login(form: OAuth2PasswordRequestForm = Depends()):
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
    current_user = user.get_user_by_name(username)
    return User(id=current_user.id,
                name=current_user.name,
                fullName=current_user.fullName,
                role=current_user.role)


@app.post('/api/users')
def add_user(new_user: User, username: str = Depends(decode_token)):
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
    if user.is_admin(username):
        user.update_user(id, new_user.name, new_user.fullName,
                         new_user.newPassword, new_user.role)
    return


@app.put('/api/users/{id}/password')
def reset_password(id: int,
                   password_data: ResetPasswordData,
                   username: str = Depends(decode_token)):
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
    if user.is_admin(username):
        user.delete_user(id)
    return


@app.get('/api/users/{id}')
def get_user(id: int, username: str = Depends(decode_token)):
    if user.is_admin(username):
        u = user.get_user(id)
        return User(id=u.id, name=u.name, fullName=u.fullName, role=u.role)


@app.get('/api/devices')
def get_devices(username: str = Depends(decode_token)):
    device_manager_service = DeviceManagerService()
    return {'data': device_manager_service.get_devices()}


@app.post('/api/devices')
def add_device(device: NewDeviceModel, username: str = Depends(decode_token)):
    device_manager_service = DeviceManagerService()
    device_manager_service.add_device(device)
    return


@app.get('/api/devices/{uuid}')
def get_device(uuid: str, username: str = Depends(decode_token)):
    device_manager_service = DeviceManagerService()
    return device_manager_service.get_device(uuid)


@app.put('/api/devices/{uuid}')
def set_device(uuid: str,
               device: DeviceInfoModel,
               username: str = Depends(decode_token)):
    device_manager_service = DeviceManagerService()
    device_manager_service.set_device(uuid, device)
    return


@app.delete('/api/devices/{uuid}')
def delete_device(uuid: str, username: str = Depends(decode_token)):
    device_manager_service = DeviceManagerService()
    device_manager_service.delete_device(uuid)
    return


@app.get('/api/deviceStatus/{uuid}')
def device_status(uuid: str, username: str = Depends(decode_token)):
    device_manager_service = DeviceManagerService()
    return device_manager_service.get_status(uuid)


@app.get('/api/deviceFeatures/{uuid}')
def device_features(uuid: str, username: str = Depends(decode_token)):
    device_manager_service = DeviceManagerService()
    return {'data': device_manager_service.get_features(uuid)}


@app.post('/api/device/{uuid}/feature/{feature}/command/{command_id}')
def call_feature_command(uuid: str,
                         feature: str,
                         command_id: str,
                         parameterList: DeviceCommandParameters,
                         username: str = Depends(decode_token)):
    device_manager_service = DeviceManagerService()
    return device_manager_service.call_feature_command(uuid, feature,
                                                       command_id,
                                                       parameterList.params)


@app.get('/api/device/{uuid}/feature/{feature}/property/{property_id}')
def get_feature_property(uuid: str,
                         feature: str,
                         property_id: str,
                         username: str = Depends(decode_token)):
    device_manager_service = DeviceManagerService()
    return device_manager_service.get_feature_property(uuid, feature,
                                                       property_id)


@app.get('/api/silaDiscovery/')
def sila_discovery():
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
    device_manager_service = DeviceManagerService()
    return {'data': device_manager_service.get_bookings(start, end)}


@app.post('/api/bookings')
def book_device(bookingInfo: BookingModel,
                username: str = Depends(decode_token)):
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
    device_manager_service = DeviceManagerService()
    return {
        'data': device_manager_service.get_device_bookings(uuid, start, end)
    }


@app.get('/api/bookings/{bookingID}')  #, methods=['GET', 'DELETE'])
def get_booking(bookingID: int, username: str = Depends(decode_token)):
    device_manager_service = DeviceManagerService()
    return {'data': device_manager_service.get_booking_entry(bookingID)}


@app.delete('/api/bookings/{bookingID}')  #, methods=['GET', 'DELETE'])
def delete_booking(bookingID: int, username: str = Depends(decode_token)):
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
    device_manager_service = DeviceManagerService()
    return {'data': device_manager_service.get_all_experiments()}


@app.post('/api/experiments')
def create_experiment(experiment: ExperimentBookingModel,
                      username: str = Depends(decode_token)):

    userID = user.get_user_by_name(username).id
    device_manager_service = DeviceManagerService()
    device_manager_service.create_experiment(experiment.name, experiment.start,
                                             experiment.end, userID,
                                             experiment.devices,
                                             experiment.scriptID)
    return


@app.delete('/api/experiments/{experimentID}')
def delete_experiment(experimentID: int,
                      username: str = Depends(decode_token)):

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
    device_manager_service = DeviceManagerService()
    current_user = user.get_user_by_name(username)
    return {
        'data': device_manager_service.get_user_scripts_info(current_user.id)
    }


@app.get('/api/scripts/{scriptID}')
def get_user_script(scriptID: int, username: str = Depends(decode_token)):
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
    device_manager_service = DeviceManagerService()
    current_user = user.get_user_by_name(username)
    device_manager_service.create_user_script(script.name, script.fileName,
                                              current_user.id, script.data)
    return


@app.delete('/api/scripts/{scriptID}')
def delete_user_script(scriptID: int, username: str = Depends(decode_token)):
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
    if status.running:
        await start_experiment(experimentID)
    else:
        await stop_experiment(experimentID)
    return

@app.websocket("/ws/experiments")
async def websocket_endpoint(websocket: WebSocket):#, username:str = Depends(decode_token)):
    await websocket.accept()
    pool = await get_redis_pool()
    channels = await pool.subscribe('experiment_status')
    while await channels[0].wait_message():
        #message = await receive_experiment_status(channel)
        message = msgpack.unpackb(await channels[0].get(), raw=False)
        print(f"{message}")
        await websocket.send_text("{message}")
