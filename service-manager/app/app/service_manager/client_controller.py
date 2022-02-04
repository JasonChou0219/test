from typing import List, Dict

from sila2.client import SilaClient
from sila2.discovery import SilaDiscoveryBrowser

from app.schemas import ServiceInfo
from app.service_manager.feature_controller import FeatureController

sila_services: Dict[str, SilaClient] = {}
service_feature_controllers: Dict[str, FeatureController] = {}


def discover_clients():
    services = List[ServiceInfo]
    browser = SilaDiscoveryBrowser()
    try:
        browser.find_server("IllegalNameValue", timeout=5)
    except:
        pass

    clients = browser.clients

    for client in clients:
        sila_service = ServiceInfo()
        sila_service.server_name = client.SiLAService.ServerName.get()
        sila_service.name = client.SiLAService.ServerName.get()
        sila_service.type = client.SiLAService.ServerType.get()
        sila_service.description = client.SiLAService.ServerDescription.get()

        sila_service.uuid = client.SiLAService.ServerUUID.get()
        sila_service.type = client.SiLAService.ServerType.get()
        sila_service.version = client.SiLAService.ServerVersion.get()

        sila_service.online = True
        sila_service.favourite = False

        # sila_service.parsed_ip_address = client.SiLAService.get()
        # sila_service.port = 0

        for feature_identifier in client.SiLAService.ImplementedFeatures.get():
            sila_service.feature_names.append(feature_identifier)

        services.append(sila_service)

    return services


def connect_client(client_ip: str, client_port: int):
    client = SilaClient(str(client_ip), client_port)
    service_uuid = client.SiLAService.ServerUUID.get()
    sila_services.update({service_uuid: client})
    service_feature_controller = FeatureController(client)
    service_feature_controllers.update({service_uuid: service_feature_controller})
    return


def browse_features(service_uuid: str):
    feature_controller = service_feature_controllers[service_uuid]
    return list(feature_controller.features.values())


def run_function(service_uuid: str,
                 identifier: str,
                 function: str,
                 is_property: bool,
                 is_observable: bool,
                 response_identifiers: List[str] = None,
                 parameters: List[str] = None):
    feature_controller = service_feature_controllers[service_uuid]
    return feature_controller.run_function(
        identifier, function, is_property, is_observable, response_identifiers, parameters)
