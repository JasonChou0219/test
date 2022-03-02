from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.types import TypeDecorator
from app.db.base_class import Base
from app.schemas import ScheduledJobStatus

if TYPE_CHECKING:
    from .job import Job  # noqa: F401
    from .workflow import Flow  # noqa: F401
    from .user import User  # noqa: F401


class IntEnum(TypeDecorator):
    impl = Integer

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        return value  # .value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)


class ScheduledJob(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=False)
    owner = Column(String, index=True)
    owner_id = Column(Integer, index=True)

    workflows = Column(JSON, index=False)

    created_at = Column(TIMESTAMP(timezone=True), index=True)
    execute_at = Column(TIMESTAMP(timezone=True), index=True)
    scheduled_at = Column(TIMESTAMP(timezone=True), index=True)
    job_id = Column(Integer, index=False)
    job_status = Column(IntEnum(ScheduledJobStatus), index=False)
