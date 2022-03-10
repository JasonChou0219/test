from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from app.db.base_class import Base
from .workflow import Workflow

if TYPE_CHECKING:
    # from .workflow import Workflow  # noqa: F401
    from .user import User  # noqa: F401


class Job(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=False)
    owner = Column(String, index=True)
    owner_id = Column(Integer, index=True)

    workflows = Column(JSON, index=False)
    workflow = relationship(Workflow, backref="job", passive_deletes=True)

    created_at = Column(TIMESTAMP(timezone=True), index=True)
    execute_at = Column(TIMESTAMP(timezone=True), index=True)
