from source.device_manager.device_layer.device_feature import DeviceParameter, DeviceCommand, DeviceProperty, DeviceFeature

from typing import List
from sila2lib.fdl_parser.fdl_parser import FDLParser
from sila2lib.fdl_parser.command import Command
from sila2lib.fdl_parser.property import Property


def serialize_feature(parser: FDLParser) -> DeviceFeature:
    return DeviceFeature(
        parser.identifier,
        parser.name,
        parser.description,
        #parser.sila2_version,
        #parser.category,
        #parser.maturity_level,
        #parser.locale,
        #parser.originator,
        parser.feature_version,
        parser.feature_version_minor,
        parser.feature_version_major,
        serialize_commands(parser.commands),
        serialize_properties(parser.properties))


def serialize_properties(properties) -> List[DeviceProperty]:
    result: List[DeviceProperty] = []
    for prop in properties.values():
        result.append(serialize_property(prop))
    return result


def serialize_property(prop: Property) -> DeviceProperty:
    return DeviceProperty(str(prop.identifier), str(prop.name),
                          str(prop.description), prop.observable,
                          serialize_parameter(prop.response),
                          prop.defined_execution_errors)


def serialize_commands(commands) -> List[DeviceCommand]:
    result: List[DeviceCommand] = []
    for command in commands.values():
        result.append(serialize_command(command))
    return result


def serialize_command(command: Command) -> DeviceCommand:
    return DeviceCommand(str(command.identifier), str(command.name),
                         str(command.description), command.observable,
                         serialize_parameters(command.parameters),
                         serialize_parameters(command.responses),
                         command.intermediates,
                         command.defined_execution_errors)


def serialize_parameters(parameters) -> List[DeviceParameter]:
    result: List[DeviceParameter] = []
    for parameter in parameters.values():
        result.append(serialize_parameter(parameter))
    return result


def serialize_parameter(parameter):
    return DeviceParameter(parameter.sub_type.name, parameter.identifier,
                           parameter.name, parameter.description)
