from typing import List, Optional

from pydantic import BaseModel


class SilaFeatureBase(BaseModel):
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

    class Config:
        orm_mode = True


class SilaFeatureCreate(SilaFeatureBase):
    owner_uuid: Optional[str] = None
    pass


class SilaFeatureDB(SilaFeatureBase):
    id: int

    class Config:
        orm_mode = True


class SilaFeatureUpdate(SilaFeatureBase):
    pass
