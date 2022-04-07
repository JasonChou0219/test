from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.base_class import Base
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    pass


class ProtocolFeature(Base):
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, index=True)
    service_id = Column(Integer, ForeignKey('protocolservice.id'))
    commands = relationship("ProtocolCommand", cascade="all, delete-orphan")
    properties = relationship("ProtocolProperty", cascade="all, delete-orphan")
