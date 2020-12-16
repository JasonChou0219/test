from dataclasses import dataclass
from typing import List


@dataclass
class DeviceParameter:
    type: str
    identifier: str
    name: str
    description: str


@dataclass
class DeviceParameterForDataHandler(DeviceParameter):
    id: int
    value: str


@dataclass
class DataHandlerConfig:
    interval: int
    meta_interval: int
    activated: bool
    meta: bool


@dataclass
class DeviceProperty:
    identifier: str
    name: str
    description: str
    observable: bool
    response: DeviceParameter
    defined_execution_errors: List[str]


@dataclass
class DevicePropertyForDataHandler(DeviceProperty, DataHandlerConfig):
    id: int
    response: DeviceParameterForDataHandler


@dataclass
class DeviceCommand:
    identifier: str
    name: str
    description: str
    observable: bool
    parameters: List[DeviceParameter]
    responses: List[DeviceParameter]
    intermediates: List[DeviceParameter]
    defined_execution_errors: List[str]


@dataclass
class DeviceCommandForDataHandler(DeviceCommand, DataHandlerConfig):
    id: int
    parameters: List[DeviceParameterForDataHandler]
    responses: List[DeviceParameterForDataHandler]
    intermediates: List[DeviceParameterForDataHandler]


@dataclass
class DeviceFeature:
    identifier: str
    name: str
    description: str
    #sila2_version: str
    #category: str
    #maturity_level: str
    #locale: str
    #originator: str
    feature_version: str
    feature_version_minor: int
    feature_version_major: int
    commands: List[DeviceCommand]
    properties: List[DeviceProperty]


@dataclass
class DeviceFeatureForDataHandler(DeviceFeature):
    id: int
    commands: List[DeviceCommandForDataHandler]
    properties: List[DevicePropertyForDataHandler]
    active: bool
    meta: bool
