import json
from uuid import UUID

from requests import post

target_service_hostname = "http://localhost"  # -> to env var
target_service_port = '80'  # settings.BACKEND_GATEWAY_UVICORN_PORT  # -> to env var
target_service_api_version = "/api/v1"  # settings.API_V1_STR  # -> to env var
target_service_url = f'{target_service_hostname}:{target_service_port}{target_service_api_version}/'
route = f"{target_service_url}functions/unobservable/"


def run_command(service_uuid: UUID, feature_identifier: str, function_identifier: str, parameters: dict,
                response_identifier: str = None):
    try:
        res = post(route,
                   params={'service_uuid': service_uuid,
                           'feature_identifier': feature_identifier,
                           'function_identifier': function_identifier,
                           'response_identifiers': response_identifier},
                   data=json.dumps(parameters)
                   ).json()['response']
        return res
    except KeyError:
        return "KeyError: Provided params do not match SiLA service specification."
