from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON, UUID

from app.db.base_class import Base

if TYPE_CHECKING:
    from .job import Job  # noqa: F401


class Job(Base):
    uuid = Column(UUID, primary_key=True, index=True)
    flow = Column(JSON)
    description = Column(String, index=True)
    title = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True)
    execute_at = Column(TIMESTAMP, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="jobs")
