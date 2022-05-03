import json
from uuid import UUID

from requests import post, get

# Default settings
target_service_hostname = "http://localhost"  # -> to env var
target_service_port = '80'  # settings.BACKEND_GATEWAY_UVICORN_PORT  # -> to env var
target_service_api_version = "/api/v1"  # settings.API_V1_STR  # -> to env var
target_service_url = f'{target_service_hostname}:{target_service_port}{target_service_api_version}/'


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
                   data=json.dumps(parameters)
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
