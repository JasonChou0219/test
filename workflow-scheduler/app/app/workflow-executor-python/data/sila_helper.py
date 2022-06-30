from uuid import UUID
from requests import post, get

# Default settings
target_service_hostname = "http://10.152,248.14"  # -> to env var
target_service_port = '80'  # settings.BACKEND_GATEWAY_UVICORN_PORT  # -> to env var
target_service_api_version = "/api/v1"  # settings.API_V1_STR  # -> to env var
target_service_url = f'{target_service_hostname}{target_service_api_version}/'


def _get_target_service_url():
    return f'{target_service_hostname}:{target_service_port}{target_service_api_version}/'


def _get_route_unobservable():
    return f"{_get_target_service_url()}functions/unobservable"


def _get_route_connect_initial():
    return f"{_get_target_service_url()}functions/connect_initial"


def run_command(service_uuid: UUID, feature_identifier: str, function_identifier: str, parameters: dict = None,
                response_identifier: str = None):
    try:
        res = post(_get_route_unobservable(),
                   params={'service_uuid': service_uuid,
                           'feature_identifier': feature_identifier,
                           'function_identifier': function_identifier,
                           'response_identifiers': response_identifier
                           },
                   json=parameters
                   ).json()['response']
        return res
    except KeyError:
        return "KeyError: Provided params do not match SiLA service specification."


def instantiate_sila_client(address: str, port: int):
    print(f'Connecting to {address}:{port}')
    _route = _get_route_connect_initial()
    retries = 3
    i = 0
    while True:
        if i == 3:
            print('Max retries exceeded! Aborting...')
            break
        try:
            response = get(_route, params={'client_ip': address, 'client_port': port})
            if response.status_code == 404:
                print('Encountered Error 404')
                raise Exception
            elif response.status_code == 500:
                print('Encountered Error 404')
                raise Exception
            else:
                print('No error encounter. Status code is: ', response.status_code)
                # Remove once final #
                print(response, flush=True)
                sila_client = response.json()
                print(sila_client, flush=True)
                # Remove until here #
                return response.json()
        except Exception:
            i += 1
            print(f'Retry: {i}')
            continue

    return None


class DASGIP:

    def __init__(self, address: str, port: int, unit: int):
        self.client = instantiate_sila_client(address=address, port=port)
        self.uuid = self.client['uuid']
        self.unit = unit

    # Temperature control

    def disable_temperature_control(self):
        return run_command(service_uuid=self.uuid, feature_identifier='TemperatureServicer', function_identifier='SetCmd',
                           parameters={"UnitID": self.unit, "Cmd": 1}, response_identifier="CmdSet")['CmdSet']

    def enable_temperature_control(self):
        return run_command(service_uuid=self.uuid, feature_identifier='PHServicer', function_identifier='SetCmd',
                           parameters={"UnitID": self.unit, "Cmd": 2}, response_identifier="CmdSet")['CmdSet']
    # pH control

    def disable_pH_control(self):
        return run_command(service_uuid=self.uuid, feature_identifier='PHServicer', function_identifier='SetCmd',
                           parameters={"UnitID": self.unit, "Cmd": 1}, response_identifier="CmdSet")['CmdSet']

    def enable_pH_control(self):
        return run_command(service_uuid=self.uuid, feature_identifier='PHServicer', function_identifier='SetCmd',
                           parameters={"UnitID": self.unit, "Cmd": 2}, response_identifier="CmdSet")['CmdSet']

    # Stirrer control

    def stop_stirrer(self):
        return run_command(service_uuid=self.uuid, feature_identifier='AgitationServicer', function_identifier='SetCmd',
                           parameters={"UnitID": self.unit, "Cmd": 1}, response_identifier="CmdSet")['CmdSet']

    def start_stirrer(self):
        return run_command(service_uuid=self.uuid, feature_identifier='AgitationServicer', function_identifier='SetCmd',
                           parameters={"UnitID": self.unit, "Cmd": 2}, response_identifier="CmdSet")['CmdSet']

    # Gassing control

    def stop_aeration(self):
        return run_command(service_uuid=self.uuid, feature_identifier='GassingServicer', function_identifier='SetCmd',
                           parameters={"UnitID": self.unit, "Cmd": 1}, response_identifier="CmdSet")['CmdSet']

    def start_aeration(self):
        return run_command(service_uuid=self.uuid, feature_identifier='GassingServicer', function_identifier='SetCmd',
                           parameters={"UnitID": self.unit, "Cmd": 2}, response_identifier="CmdSet")['CmdSet']

    # Level sensor

    def get_level_sensor(self):
        return run_command(service_uuid=self.uuid, feature_identifier='LevelServicer', function_identifier='GetPV',
                           parameters={"UnitID": self.unit}, response_identifier="CurrentPV")['CurrentPV']

    # DO control

    def get_DO_sensor(self):
        return run_command(service_uuid=self.uuid, feature_identifier='DOServicer', function_identifier='GetPV',
                           parameters={"UnitID": self.unit}, response_identifier="CurrentPV")['CurrentPV']
