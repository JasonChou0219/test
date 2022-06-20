from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    pass


class Protocol(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    service = relationship("ProtocolService", uselist=False, cascade="all, delete-orphan", lazy='joined')
    custom_data = Column(JSON, index=False)
    owner = Column(String, index=True)
    owner_id = Column(String, index=True)
    job_id = Column(Integer, index=False)
