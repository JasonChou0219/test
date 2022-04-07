from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from app.db.base_class import Base
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    pass


class ProtocolCommand(Base):
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, index=True)
    observable = Column(Boolean, index=False)
    meta = Column(Boolean, index=False)
    interval = Column(Integer, index=False)
    feature_id = Column(Integer, ForeignKey('protocolfeature.id'))
    parameters = relationship("ProtocolParameter", cascade="all, delete-orphan")
    responses = relationship("ProtocolResponse", cascade="all, delete-orphan")
