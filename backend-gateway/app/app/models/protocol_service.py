from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.base_class import Base
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    pass


class ProtocolService(Base):
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, index=True)
    protocol_id = Column(Integer, ForeignKey('protocol.id'))
    features = relationship("ProtocolFeature", cascade="all, delete-orphan")
