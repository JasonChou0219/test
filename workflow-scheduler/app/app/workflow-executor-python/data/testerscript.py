from requests import post, get
import logging
import sila_helper

target_service_hostname = "http://localhost"  # -> to env var
target_service_port = '80'  # settings.BACKEND_GATEWAY_UVICORN_PORT  # -> to env var
target_service_api_version = "/api/v1"  # settings.API_V1_STR  # -> to env var
target_service_url = f'{target_service_hostname}:{target_service_port}{target_service_api_version}/'

# Connect the clients of the RegloICC and the MT Viper SW. This should happen automatically in the __main__.py in the
# container when it is started. Connection details are supplied by the workflow scheduler.
route = f"{target_service_url}functions/connect_initial/"  # Should be connect only, but return of connect does not
# contain service uuid yet!

tester = get(route, params={'client_ip': '10.180.154.151', 'client_port': 50052}).json()

services_dict = {
    'TesterService': tester
}

ROUTE = f"{target_service_url}functions/unobservable/"


# route_observable = f"{target_service_url}functions/observable"


def run():
    client = services_dict['TesterService']
    # try:
    #     res = post(ROUTE, params={'service_uuid': client['uuid'], 'feature_identifier': 'DataTypeProvider',
    #                               'function_identifier': 'StructureProperty'},
    #                json={"Name": "Robert"}
    #                ).json()['response']
    #     print(res)
    # except:
    #     res = post(ROUTE, params={'service_uuid': client['uuid'], 'feature_identifier': 'DataTypeProvider',
    #                               'function_identifier': 'StructureProperty'},
    #                json={"Name": "Robert"}
    #                )
    #     print(res)

    res2 = sila_helper.run_command(client['uuid'], 'DataTypeProvider', "StructureProperty",
                                   parameters={})

    print(res2)


if __name__ == '__main__':
    run()
