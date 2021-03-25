from source.device_manager.device_layer.device_feature import Command, CommandParameter, CommandResponse, \
    IntermediateCommandResponse, Property, PropertyResponse, Feature

from typing import List
from sila2lib.fdl_parser.fdl_parser import FDLParser
from sila2lib.fdl_parser.command import Command as FDLCommand
from sila2lib.fdl_parser.property import Property as FDLProperty


def serialize_feature(parser: FDLParser) -> Feature:
    return Feature(
        parser.identifier,
        parser.name,
        parser.description,
        serialize_commands(parser.commands),
        serialize_properties(parser.properties),
        parser.sila2_version,
        parser.originator,
        parser.category,
        parser.maturity_level,
        parser.locale,
        parser.feature_version,
        parser.feature_version_minor,
        parser.feature_version_major
    )


def serialize_properties(properties) -> List[Property]:
    result: List[Property] = []
    for prop in properties.values():
        result.append(serialize_property(prop))
    return result


def serialize_property(prop: FDLProperty) -> Property:
    return Property(str(prop.identifier), str(prop.name),
                    str(prop.description), prop.observable,
                    serialize_property_response(prop.response),
                    prop.defined_execution_errors)


def serialize_commands(commands) -> List[Command]:
    result: List[Command] = []
    for command in commands.values():
        result.append(serialize_command(command))
    return result


def serialize_command(command: FDLCommand) -> Command:
    return Command(str(command.identifier), str(command.name),
                   str(command.description), command.observable,
                   serialize_command_parameters(command.parameters),
                   serialize_command_responses(command.responses),
                   command.intermediates,
                   command.defined_execution_errors)


def serialize_command_parameters(parameters) -> List[CommandParameter]:
    result: List[CommandParameter] = []
    for parameter in parameters.values():
        result.append(serialize_command_parameter(parameter))
    return result


def serialize_command_responses(responses) -> List[CommandResponse]:
    result: List[CommandResponse] = []
    for response in responses.values():
        result.append(serialize_command_response(response))
    return result


def serialize_intermediate_command_responses(intermediate_responses) -> List[IntermediateCommandResponse]:
    result: List[IntermediateCommandResponse] = []
    for intermediate_response in intermediate_responses.values():
        result.append(serialize_intermediate_command_response(intermediate_response))
    return result

#class CommandParameter:
#    identifier: str
#    display_name: str
#    description: str
#    data_type: str

def serialize_command_parameter(parameter):
    print('Parameter functions and attributes')
    print('---------------------------------------')
    print(dir(parameter))
    if parameter.sub_type.is_constrained:
        sub_type = 'constrained/' + parameter.sub_type.sub_type.name
        print('CIdentifier:', parameter.identifier)
        print('CConstrained:', parameter.sub_type.is_constrained)
        print('CSubTYpe:', parameter.sub_type.sub_type)
        print('CSubTYpe:', parameter.sub_type.sub_type.name)
        print('CName:', parameter.name)
    else:
        sub_type = parameter.sub_type.name
        print('Identifier:', parameter.identifier)
        print('Constrained:', parameter.is_constrained)
        print('SubTYpe:', parameter.sub_type)
        print('SubTYpe:', parameter.sub_type.name)
        print('Name:', parameter.name)
    return CommandParameter(parameter.identifier, parameter.name,
                            parameter.description, sub_type)


def serialize_command_response(response):
    print('Command Response functions and attributes')
    print('---------------------------------------')
    print(dir(response))
    if response.sub_type.is_constrained:
        sub_type = 'constrained/' + response.sub_type.sub_type.name
        print('CIdentifier:', response.identifier)
        print('CConstrained:', response.sub_type.is_constrained)
        print('CSubTYpe:', response.sub_type.sub_type)
        print('CSubTYpe:', response.sub_type.sub_type.name)
        print('CName:', response.name)

    else:
        sub_type = response.sub_type.name
        print('Identifier:', response.identifier)
        print('Constrained:', response.is_constrained)
        print('SubTYpe:', response.sub_type)
        print('SubTYpe:', response.sub_type.name)
        print('Name:', response.name)
    return CommandResponse(response.identifier, response.name,
                           response.description, sub_type)


def serialize_intermediate_command_response(intermediate_response):
    print('Intermediate Response functions and attributes')
    print('---------------------------------------')
    print(dir(intermediate_response))
    if intermediate_response.sub_type.is_constrained:
        sub_type = 'constrained/' + intermediate_response.sub_type.sub_type.name
        print('CType:', intermediate_response.sub_type.sub_type.name)
        print('CIdentifier:', intermediate_response.identifier)
        print('CConstrained:', intermediate_response.sub_type.is_constrained)
        print('CSubTYpe:', intermediate_response.sub_type.sub_type)
        print('CName:', intermediate_response.name)

    else:
        sub_type = intermediate_response.sub_type.name
        print('Type:', intermediate_response.sub_type.name)
        print('Identifier:', intermediate_response.identifier)
        print('Constrained:', intermediate_response.is_constrained)
        print('SubTYpe:', intermediate_response.sub_type)
        print('Name:', intermediate_response.name)
    return IntermediateCommandResponse(intermediate_response.identifier, intermediate_response.name,
                                       intermediate_response.description, sub_type)


def serialize_property_response(response):
    print('Response functions and attributes')
    print('---------------------------------------')
    print(dir(response))
    if response.sub_type.is_constrained:
        sub_type = 'constrained/' + response.sub_type.sub_type.name
        print('CIdentifier:', response.identifier)
        print('CConstrained:', response.sub_type.is_constrained)
        print('CSubTYpe:', response.sub_type.sub_type)
        print('CSubTYpe:', response.sub_type.sub_type.name)
        print('CName:', response.name)

    else:
        sub_type = response.sub_type.name
        print('Identifier:', response.identifier)
        print('Constrained:', response.is_constrained)
        print('SubTYpe:', response.sub_type)
        print('SubTYpe:', response.sub_type.name)
        print('Name:', response.name)
    return CommandResponse(response.identifier, response.name,
                           response.description, sub_type)
