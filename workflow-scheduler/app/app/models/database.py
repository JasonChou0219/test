from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.base_class import Base

if TYPE_CHECKING:
    pass


class Database(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=False)
    name = Column(String, index=False)
    username = Column(String, index=False)
    password = Column(String, index=False)
    address = Column(String, index=False)
    port = Column(Integer, index=False)
    retention_policy = Column(String, index=False)
    owner = Column(String, index=True)
    owner_id = Column(String, index=True)
    job_id = Column(Integer, ForeignKey("job.id"))
