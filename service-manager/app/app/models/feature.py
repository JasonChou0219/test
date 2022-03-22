from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class Feature(Base):
    __tablename__ = "features"
    id = Column(Integer, primary_key=True, index=True)
    owner_uuid = Column(String(800))
    category = Column(String(800))
    feature_version = Column(String(800))
    maturity_level = Column(String(800))
    originator = Column(String(800))
    sila2_version = Column(String(800))
    identifier = Column(String(800), index=True)
    display_name = Column(String(800))
    description = Column(String(800))
    locale = Column(String(800))
    commands = Column(JSON)
    properties = Column(JSON)
    errors = Column(JSON)

