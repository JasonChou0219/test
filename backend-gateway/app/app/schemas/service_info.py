from typing import Optional

from mypy.errors import List
from pydantic import BaseModel


class ServiceInfo(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    parsed_ip_address: Optional[str] = None
    port: Optional[int] = None
    uuid: Optional[str] = None
    version: Optional[str] = None
    server_name: Optional[str] = None
    description: Optional[str] = None
    feature_names: Optional[List[str]] = []
