from typing import Optional, Any, Union, Dict

from mypy.errors import List
from pydantic import BaseModel


class Feature(BaseModel):
    category: Optional[str] = None
    feature_version: Optional[str] = None
    maturity_level: Optional[str] = None
    originator: Optional[str] = None
    sila2_version: Optional[str] = None
    identifier: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    locale: Optional[str] = None
    commands: Optional[dict] = None
    properties: Optional[dict] = None
    errors: Optional[dict] = None


class FunctionResponse(BaseModel):
    feature_identifier: Optional[str] = None
    function_identifier: Optional[str] = None
    response: Dict[str, Any] = None

    class Config:
        orm_mode = True
