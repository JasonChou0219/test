from typing import List, Dict

from sila2.client import SilaClient
from sila2.discovery import SilaDiscoveryBrowser
from sila2.framework import SilaConnectionError

from app.schemas import ServiceInfo
from app.service_manager.feature_controller import FeatureController

sila_services: Dict[str, SilaClient] = {}
service_feature_controllers: Dict[str, FeatureController] = {}


def discover_clients():
    services = []
    browser = SilaDiscoveryBrowser(insecure=True)
    try:
        browser.find_server("IllegalNameValue", timeout=2)
    except:
        pass

    clients = browser.clients

    for client in clients:
        sila_service = get_service_info(client)
        services.append(sila_service)

    return list(services)


def get_service_info(client):
    sila_service = ServiceInfo()
    sila_service.server_name = client.SiLAService.ServerName.get()
    sila_service.name = client.SiLAService.ServerName.get()
    sila_service.type = client.SiLAService.ServerType.get()
    sila_service.description = client.SiLAService.ServerDescription.get()
    sila_service.parsed_ip_address = client.address
    sila_service.port = client.port
    sila_service.uuid = client.SiLAService.ServerUUID.get()
    sila_service.type = client.SiLAService.ServerType.get()
    sila_service.version = client.SiLAService.ServerVersion.get()
    sila_service.online = True
    sila_service.favourite = False
    sila_service.isGateway = False
    for feature_identifier in client.SiLAService.ImplementedFeatures.get():
        sila_service.feature_names.append(feature_identifier)

    return sila_service


def connect_client(client_ip: str, client_port: int, reset: str = None):
    client = SilaClient(str(client_ip), client_port, insecure=True)
    service_uuid = client.SiLAService.ServerUUID.get()
    if reset and service_uuid in sila_services:
        raise ValueError("Client already in use")

    sila_services.update({service_uuid: client})
    service_feature_controller = FeatureController(client)
    service_feature_controllers.update({service_uuid: service_feature_controller})
    return service_uuid


def connect_initial(client_ip: str, client_port: int, reset: str = None):
    uuid = connect_client(client_ip, client_port, reset)
    service_info = get_service_info(sila_services.get(uuid))
    return service_info


def browse_features(service_uuid: str):
    feature_controller = service_feature_controllers[service_uuid]
    return list(feature_controller.features.values())


def run_function(service_uuid: str,
                 feature_identifier: str,
                 function_indetifier: str,
                 is_property: bool,
                 response_identifiers: List[str] = None,
                 parameters: List[str] = None):
    feature_controller = service_feature_controllers[service_uuid]
    try:
        function_resp = feature_controller.run_function(
            feature_identifier, function_indetifier, is_property, response_identifiers, parameters)
    except SilaConnectionError:
        sila_services.pop(service_uuid)
        raise ValueError("Lost connection with client with uuid" + service_uuid)

    return function_resp
