from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class Feature(Base):
    __tablename__ = "features"
    id = Column(Integer, primary_key=True, index=True)
    owner_uuid = Column(String(200), ForeignKey("service_info.uuid"))
    category = Column(String(200))
    feature_version = Column(String(200))
    maturity_level = Column(String(200))
    originator = Column(String(200))
    sila2_version = Column(String(200))
    identifier = Column(String(200), index=True)
    display_name = Column(String(200))
    description = Column(String(200))
    locale = Column(String(200))
    commands = Column(JSON)
    properties = Column(JSON)
    errors = Column(JSON)

