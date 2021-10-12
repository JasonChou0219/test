from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Service(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="services")

    hostname = Column(String, index=True)
    ip = Column(String, index=True)
    port = Column(Integer, index=True)
    service_uuid = Column(UUID(as_uuid=True), default=uuid4, index=True)
