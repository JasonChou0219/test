from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .job import Job


class Workflow(Base):
    uid = Column(Integer, primary_key=True, index=True)
    id = Column(String, index=True)
    title = Column(String, index=True)
    workflow_type = Column(String, index=True)
    file_name = Column(String, index=False)
    data = Column(JSON, index=False)
    owner = Column(String, index=True)
    owner_id = Column(Integer, index=True)
    description = Column(String, index=True)
    job_id = Column(Integer, ForeignKey("job.id", ondelete='CASCADE'))

    #id = Column(Integer, primary_key=True, index=True)
    #workflow = Column(JSON)
    #description = Column(String, index=True)
    #title = Column(String, index=True)
    #owner_id = Column(Integer, ForeignKey("user.id"))
    #owner = relationship("User", back_populates="workflows")
    #jobs = relationship("Job", back_populates="workflow")
