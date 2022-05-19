from typing import List, Dict, Union

from sila2.client import SilaClient

from app.schemas.sila_service_feature_dto import Feature
from app.service_manager.featurer_parser import ClientFeatureParser


class FeatureController:
    sila_client: SilaClient
    features: Dict[str, Feature]

    def __init__(self, sila_client: SilaClient):
        feature_xml = []
        self.features = {}
        self.sila_client = sila_client

        for feature_identifier in self.sila_client.SiLAService.ImplementedFeatures.get():
            feature_xml.append(feature_identifier)

        feature_definitions_xml = list(
            map(lambda feature_id: self.sila_client.SiLAService.GetFeatureDefinition(feature_id), feature_xml))

        for xml_definition in feature_definitions_xml:
            for x in range(0, len(xml_definition)):
                parser = ClientFeatureParser(xml_definition[x])
                self.features.update(parser.parse_xml())

    def get_feature_by_identifier(self, identifier: str):
        return self.features[identifier]

    def get_observable_instance(self,
                                feature_identifier: str,
                                function_identifier: str,
                                parameters: Union[Dict, List] = None):
        function_object = getattr(vars(self.sila_client)[feature_identifier],
                                  function_identifier)
        if parameters:
            return function_object(**parameters)
        else:
            return function_object

    def run_function(self,
                     feature_identifier: str,
                     function_identifier: str,
                     response_identifiers: List[str] = None,
                     parameters: Union[Dict, List] = None):

        is_property = self.function_is_property(feature_identifier, function_identifier)

        try:
            response = getattr(vars(self.sila_client)[feature_identifier], function_identifier)
        except KeyError:
            raise ValueError("Client has no identifier matching " + feature_identifier)

        response_values = {}

        if is_property:
            if response_identifiers:
                if response_identifiers is not None:
                    raise ValueError("ExecutionError: SiLA-Property expects no response identifier")
            response_values.update({str(function_identifier): response.get()})
        else:
            if type(parameters) is dict:
                command_response = response(**parameters)
            else:
                command_response = response(*parameters)
            response_identifier_all = []

            for command in self.features[feature_identifier].commands:
                if command.identifier == function_identifier:
                    for resp in command.responses:
                        response_identifier_all.append(resp.identifier)

            if response_identifiers is None:
                response_identifiers = response_identifier_all

            for response_id in response_identifiers:
                if response_id not in response_identifier_all:
                    raise ValueError("ExecutionError: Client has no response identifier matching " + response_id)
                response_values.update({str(response_id): getattr(command_response, response_id)})

        return response_values

    def function_is_property(self, feature_identifier, function_identifier):
        property_list = []
        for prop in self.features[feature_identifier].properties:
            property_list.append(prop.identifier)
        is_property = function_identifier in property_list
        return is_property
