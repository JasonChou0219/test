import os
from xml.etree import ElementTree
from app.schemas import Feature, Command, CommandParameter, DataType, CommandResponse, Property, DefinedExecutionError
import re


class ClientFeatureParser:
    xml_string: str

    data_types_dict = {}

    def __init__(self, xml_string: str):
        self.xml_string = xml_string

    def parse_xml(self):
        root = ElementTree.fromstring(self.xml_string)
        ElementTree.register_namespace("", "http://www.sila-standard.org")

        feature = Feature()
        feature.feature_version = root.get('FeatureVersion')
        feature.sila2_version = root.get('SiLA2Version')
        feature.originator = root.get('Originator')
        feature.maturity_level = root.get('MaturityLevel')
        feature.category = root.get('Category')

        locale_placeholder = root.get('Locale')
        if locale_placeholder:
            feature.locale = locale_placeholder

        feature_commands = []
        feature_props_ls = []
        feature_errors = []

        for elem in root.getchildren():
            if 'DataTypeDefinition' in elem.tag:
                definition_identifier = ""
                for definition in elem.getchildren():
                    if 'Identifier' in definition.tag:
                        definition_identifier = definition.text
                    result = self.parse_datatype(definition)
                    self.data_types_dict.update({definition_identifier: result
                                                 })

        for feature_property in root.getchildren():
            if 'Identifier' in feature_property.tag:
                feature.identifier = feature_property.text
            if 'DisplayName' in feature_property.tag:
                feature.display_name = feature_property.text
            if 'Description' in feature_property.tag:
                feature.description = feature_property.text
            if 'Command' in feature_property.tag:
                command = Command()
                command_parameter_list = []
                command_response_list = []
                command_intermediate_response_list = []
                command_error_identifier_list = []

                for command_props in feature_property.getchildren():
                    if 'Identifier' in command_props.tag:
                        command.identifier = command_props.text
                    if 'DisplayName' in command_props.tag:
                        command.display_name = command_props.text
                    if 'Description' in command_props.tag:
                        command.description = command_props.text
                    if 'Observable' in command_props.tag:
                        command.observable = False if command_props.text == 'No' else True
                    if 'Parameter' in command_props.tag:
                        command_parameter = CommandParameter()

                        for command_params in command_props.getchildren():
                            if 'Identifier' in command_params.tag:
                                command_parameter.identifier = command_params.text
                            if 'DisplayName' in command_params.tag:
                                command_parameter.display_name = command_params.text
                            if 'Description' in command_params.tag:
                                command_parameter.display_name = command_params.text
                            if 'DataType' in command_params.tag:
                                data_type = DataType()

                                for data_type_elems in command_params.getchildren():
                                    if 'Basic' in data_type_elems.tag:
                                        data_type.type = data_type_elems.text
                                    elif 'DataTypeIdentifier' in data_type_elems.tag:
                                        data_type.type = self.data_types_dict.get(data_type_elems.text)
                                    else:
                                        data_type.type = self.parse_datatype(data_type_elems)

                                command_parameter.data_type = data_type

                        command_parameter_list.append(command_parameter)

                    if 'Response' in command_props.tag and 'Intermediate' not in command_props.tag:
                        command_response = CommandResponse()

                        for command_params in command_props.getchildren():
                            if 'Identifier' in command_params.tag:
                                command_response.identifier = command_params.text
                            if 'DisplayName' in command_params.tag:
                                command_response.display_name = command_params.text
                            if 'Description' in command_params.tag:
                                command_response.display_name = command_params.text
                            if 'DataType' in command_params.tag:
                                data_type = DataType()

                                for data_type_elems in command_params.getchildren():
                                    if 'Basic' in data_type_elems.tag:
                                        data_type.type = data_type_elems.text
                                    else:
                                        data_type.type = self.parse_datatype(data_type_elems)

                                command_response.data_type = data_type
                        command_response_list.append(command_response)

                    if 'IntermediateResponse' in command_props.tag:
                        command_intermediate_response = CommandResponse()

                        for command_params in command_props.getchildren():
                            if 'Identifier' in command_params.tag:
                                command_intermediate_response.identifier = command_params.text
                            if 'DisplayName' in command_params.tag:
                                command_intermediate_response.display_name = command_params.text
                            if 'Description' in command_params.tag:
                                command_intermediate_response.display_name = command_params.text
                            if 'DataType' in command_params.tag:
                                data_type = DataType()

                                for data_type_elems in command_params.getchildren():
                                    if 'Basic' in data_type_elems.tag:
                                        data_type.type = data_type_elems.text
                                    else:
                                        data_type.type = self.parse_datatype(data_type_elems)
                                command_intermediate_response.data_type = data_type
                        command_intermediate_response_list.append(command_intermediate_response)

                    if 'DefinedExecutionErrors' in command_props.tag:
                        for command_error in command_props.getchildren():
                            command_error_identifier_list.append(command_error.text)

                command.parameters = command_parameter_list
                command.responses = command_response_list
                command.intermediate_responses = command_intermediate_response_list
                command.error_identifiers = command_error_identifier_list
                feature_commands.append(command)

            if 'Property' in feature_property.tag:
                sila_property = Property()
                for feature_props in feature_property.getchildren():
                    if 'Identifier' in feature_props.tag:
                        sila_property.identifier = feature_props.text
                    if 'DisplayName' in feature_props.tag:
                        sila_property.display_name = feature_props.text
                    if 'Description' in feature_props.tag:
                        sila_property.description = feature_props.text
                    if 'Observable' in feature_props.tag:
                        sila_property.observable = False if feature_props.text == 'No' else True

                    if 'DataType' in feature_props.tag:
                        data_type = DataType()

                        for data_type_elems in feature_props.getchildren():
                            if 'Basic' in data_type_elems.tag:
                                data_type.type = data_type_elems.text
                            else:
                                data_type.type = self.parse_datatype(data_type_elems)
                        sila_property.data_type = data_type
                feature_props_ls.append(sila_property)

            if 'DefinedExecutionError' in feature_property.tag:
                error = DefinedExecutionError()
                for error_props in feature_property.getchildren():
                    if 'Identifier' in error_props.tag:
                        error.identifier = error_props.text
                    if 'DisplayName' in error_props.tag:
                        error.display_name = error_props.text
                    if 'Description' in error_props.tag:
                        error.description = error_props.text
                feature_errors.append(error)

        feature.commands = feature_commands
        feature.properties = feature_props_ls
        feature.errors = feature_errors

        return {feature.identifier: feature}

    def parse_datatype(self, definition):
        string = ElementTree.tostring(definition, encoding='unicode') \
            .replace('<Structure xmlns="http://www.sila-standard.org">', '') \
            .replace('</Structure>', '') \
            .replace('xmlns="http://www.sila-standard.org', '')
        replaced_left = re.sub(r'(<)', r'\n \1', string)
        replaced_right = re.sub(r'(>)', r'\1 \n', replaced_left)
        result = os.linesep.join([s for s in replaced_right.splitlines() if s])
        return result
