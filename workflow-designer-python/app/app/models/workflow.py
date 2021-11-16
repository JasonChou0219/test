from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList

from app.db.base_class import Base

if TYPE_CHECKING:
    pass
    # from .user import User  # noqa: F401


class Workflow(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    fileName = Column(String, index=True)
    data = Column(Text, index=False)
    description = Column(String, index=True)
    owner = Column(String, index=True)
    owner_id = Column(String, index=True)

    # owner_id = Column(Integer, ForeignKey("user.id"))
    # owner = relationship("User", back_populates="workflows")
