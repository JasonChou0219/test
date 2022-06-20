from typing import Optional, Any, Dict, Union

from mypy.errors import List
from pydantic import BaseModel


# TODO REDO
class DataType(BaseModel):
    type: Optional[str] = None


class DefinedExecutionError(BaseModel):
    identifier: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class CommandParameter(BaseModel):
    identifier: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    data_type: Optional[DataType] = None

    class Config:
        orm_mode = True


class CommandResponse(BaseModel):
    identifier: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    data_type: Optional[DataType] = None

    class Config:
        orm_mode = True


class Command(BaseModel):
    identifier: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    observable: Optional[bool] = False
    parameters: Optional[List[CommandParameter]] = []
    responses: Optional[List[CommandResponse]] = []
    intermediate_responses: Optional[List[CommandResponse]]
    error_identifiers: Optional[List[str]] = []

    class Config:
        orm_mode = True


class Property(BaseModel):
    identifier: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    observable: Optional[bool] = False
    data_type: Optional[DataType] = None

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True


class FunctionResponse(BaseModel):
    feature_identifier: Optional[str] = None
    function_identifier: Optional[str] = None
    response: Dict[str, Any] = None

    class Config:
        orm_mode = True
