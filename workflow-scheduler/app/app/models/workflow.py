from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from app.db.base_class import Base

if TYPE_CHECKING:

    from .user import User  # noqa: F401


class Workflow(Base):
    id = Column(String, primary_key=True, index=True)
    workflow = Column(JSON)
    description = Column(String, index=True)
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="flows")
