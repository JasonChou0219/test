from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON, UUID

from app.db.base_class import Base

if TYPE_CHECKING:
    from .workflow import Flow  # noqa: F401
    from .user import User  # noqa: F401


class Job(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner = Column(String, index=True)
    owner_id = Column(Integer, index=True)

    workflows = Column(JSON, index=False)
    list_protocol_and_database = Column(JSON, index=False)
    dataflow_path = Column(String, index=False)

    created_at = Column(TIMESTAMP, index=True)
    execute_at = Column(TIMESTAMP, index=True)
