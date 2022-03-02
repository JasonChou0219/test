from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    pass


class Protocol(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    service = relationship("Service", uselist=False, cascade="all, delete-orphan")
    owner = Column(String, index=True)
    owner_id = Column(String, index=True)
