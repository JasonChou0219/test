from typing import List, Dict, Union, Optional, Any
from queue import Queue
from uuid import UUID

from sila2.client import SilaClient
from sila2.discovery import SilaDiscoveryBrowser
from sila2.framework import SilaConnectionError

from app.schemas import ServiceInfo
from app.service_manager.feature_controller import FeatureController

sila_services: Dict[str, SilaClient] = {}
service_feature_controllers: Dict[str, FeatureController] = {}
observables_dict: Dict = {}


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
        if client.SiLAService.ServerUUID.get() in get_connected_clients():
            sila_service.connected = True
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
    sila_service.connected = False

    return sila_service


def connect_client(client_ip: str, client_port: int, reset: str = None, encrypted: str = None):
    if encrypted:
        root_cert = open(r'./cert.pem', "rb").read()
        client = SilaClient(str(client_ip), client_port, root_certs=root_cert)
    else:
        client = SilaClient(str(client_ip), client_port, insecure=True)

    service_uuid = client.SiLAService.ServerUUID.get()
    if reset and service_uuid in sila_services:
        raise ValueError("Client already in use")

    sila_services.update({service_uuid: client})
    service_feature_controller = FeatureController(client)
    service_feature_controllers.update({service_uuid: service_feature_controller})
    return service_uuid


def disconnect_client(service_uuid: str):
    service_feature_controllers.pop(service_uuid)


def get_connected_clients():
    return service_feature_controllers.keys()


def connect_initial(client_ip: str, client_port: int, reset: str = None, encrypted: str = None):
    uuid = connect_client(client_ip, client_port, reset, encrypted)
    service_info = get_service_info(sila_services.get(uuid))
    service_info.connected = True
    return service_info


def browse_features(service_uuid: str):
    feature_controller = service_feature_controllers[service_uuid]
    return list(feature_controller.features.values())


def run_function(service_uuid: str,
                 feature_identifier: str,
                 function_identifiers: str,
                 response_identifiers: List[str] = None,
                 parameters: Union[Dict, List] = None):
    feature_controller = service_feature_controllers[service_uuid]

    try:
        function_resp = feature_controller.run_function(
            feature_identifier, function_identifiers, response_identifiers, parameters)
    except SilaConnectionError:
        sila_services.pop(service_uuid)
        raise ValueError("Lost connection with client with uuid" + service_uuid)

    return function_resp


def register_observable(service_uuid: str, feature_identifier: str, function_identifier: str,
                        named_parameters: Optional[Dict[str, Any]] = None
                        ) -> str:
    # Create the observable instance
    feature_controller = service_feature_controllers[service_uuid]
    observable_instance = feature_controller.get_observable_instance(
        feature_identifier, function_identifier, named_parameters)

    # Get response identifiers
    response_identifiers = []
    intermediate_response_identifiers = []
    for command in feature_controller.features[feature_identifier].commands:
        if command.identifier == function_identifier:
            for resp in command.responses:
                response_identifiers.append(resp.identifier)
            for resp in command.intermediate_responses:
                intermediate_response_identifiers.append(resp.identifier)

    # Add the instance to the observables dict with execution_uuid as key
    intermediate_response_subscription = observable_instance.subscribe_to_intermediate_responses()
    intermediate_response_subscription.add_callback(
        lambda resp: observables_dict[observable_instance.execution_uuid][1].put({
                        "status": observable_instance.status,
                        "progress": observable_instance.progress,
                        "estimated_remaining_time": observable_instance.estimated_remaining_time,
                        "intermediate_response": resp,
                        "response": None
                    }, timeout=1)
    )
    observables_dict.update({observable_instance.execution_uuid: (
        observable_instance, Queue(maxsize=1000), intermediate_response_identifiers, response_identifiers, intermediate_response_subscription)}
    )
    return str(observable_instance.execution_uuid)


def disconnect_websocket(execution_uuid):
    intermediate_response_subscription = observables_dict[UUID(execution_uuid)][4]
    intermediate_response_subscription.clear_callbacks()
    intermediate_response_subscription.cancel()
    observables_dict.pop(UUID(execution_uuid))

