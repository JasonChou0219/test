from typing import List, Dict

from sila2.client import SilaClient

from app.service_manager.feature_controller import FeatureController

sila_clients: Dict[str, SilaClient] = {}
client_feature_controllers: Dict[str, FeatureController] = {}


def get_connection_identifier(client_ip: str, client_port: int):
    return client_ip + ":" + str(client_port)


def discover_client():
    pass


def connect_client(client_ip: str, client_port: int):
    client_identifier = get_connection_identifier(client_ip, client_port)
    client = SilaClient(str(client_ip), 50052)
    sila_clients.update({client_identifier: client})
    client_feature_controller = FeatureController(client)
    client_feature_controllers.update({client_identifier: client_feature_controller})

    return list(client_feature_controller.features.values())


def run_function(client_ip,
                 client_port,
                 identifier: str,
                 function: str,
                 is_property: bool,
                 is_observable: bool,
                 response_identifiers: List[str] = None,
                 parameters: List[str] = None):
    client_identifier = get_connection_identifier(client_ip, client_port)
    feature_controller = client_feature_controllers[client_identifier]
    return feature_controller.run_function(
        identifier, function, is_property, is_observable, response_identifiers, parameters)

