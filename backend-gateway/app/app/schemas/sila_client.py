from typing import Optional

from mypy.errors import List
from pydantic import BaseModel


# TODO REDO
class DataType(BaseModel):
    type: Optional[str] = None


class DefinedExecutionError(BaseModel):
    identifier:  Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None


class CommandParameter(BaseModel):
    identifier: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    data_type: Optional[DataType] = None


class CommandResponse(BaseModel):
    identifier: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    data_type: Optional[DataType] = None


class Command(BaseModel):
    identifier: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    observable: Optional[bool] = False
    parameters: Optional[List[CommandParameter]] = []
    responses: Optional[List[CommandResponse]] = []
    error_identifiers: Optional[List[str]] = []


class PropertyResponse(BaseModel):
    identifier: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    data_type: Optional[DataType] = None


class Property(BaseModel):
    identifier: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    observable: Optional[bool] = False
    data_type: Optional[DataType] = None


class Feature(BaseModel):
    category: Optional[str] = None
    feature_version: Optional[str] = None
    maturity_level: Optional[str] = None
    originator: Optional[str] = None
    sila2_version: Optional[str] = None
    identifier: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    locale: str = "en-US"
    commands: Optional[List[Command]] = []
    properties: Optional[List[Property]] = []
    errors: Optional[List[DefinedExecutionError]] = []
