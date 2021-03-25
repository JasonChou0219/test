from dataclasses import dataclass
from typing import List, Dict


@dataclass
class CommandParameter:
    identifier: str
    display_name: str
    description: str
    data_type: str


@dataclass
class CommandResponse:
    identifier: str
    display_name: str
    description: str
    data_type: str


@dataclass
class IntermediateCommandResponse:
    identifier: str
    display_name: str
    description: str
    data_type: str


@dataclass
class PropertyResponse:
    identifier: str
    display_name: str
    description: str
    data_type: str


@dataclass
class DataHandlerConfig:
    polling_interval_non_meta: int
    polling_interval_meta: int
    active: bool
    meta: bool


@dataclass
class Property:
    identifier: str
    display_name: str
    description: str
    observable: bool
    response: PropertyResponse
    defined_execution_errors: List[str]


@dataclass
class PropertyResponseForDataHandler(PropertyResponse):
    id: int
    value: str


@dataclass
class PropertyForDataHandler(Property, DataHandlerConfig):
    id: int
    response: PropertyResponseForDataHandler


@dataclass
class Command:
    identifier: str
    display_name: str
    description: str
    observable: bool
    parameters: List[CommandParameter]
    responses: List[CommandResponse]
    intermediates: Dict[str, IntermediateCommandResponse]
    defined_execution_errors: List[str]


@dataclass
class CommandParameterForDataHandler(CommandParameter):
    id: int
    value: str


@dataclass
class CommandResponseForDataHandler(CommandParameter):
    id: int
    value: str


@dataclass
class IntermediateCommandResponseForDataHandler(CommandParameter):
    id: int
    value: str


@dataclass
class CommandForDataHandler(Command, DataHandlerConfig):
    id: int
    parameters: List[CommandParameterForDataHandler]
    responses: List[CommandResponseForDataHandler]
    intermediates: List[IntermediateCommandResponseForDataHandler]


@dataclass
class Feature:
    identifier: str
    display_name: str
    description: str
    commands: List[Command]
    properties: List[Property]
    sila2_version: str
    originator: str
    category: str
    maturity_level: str
    locale: str
    feature_version: str
    feature_version_minor: int
    feature_version_major: int



@dataclass
class FeatureForDataHandler(Feature):
    id: int
    commands: List[CommandForDataHandler]
    properties: List[PropertyForDataHandler]
    active: bool
    meta: bool
