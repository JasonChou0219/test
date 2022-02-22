from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    pass
    # from .user import User  # noqa: F401


class Workflow(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    workflow_type = Column(String, index=False)
    file_name = Column(String, index=True)
    data = Column(Text, index=False)
    description = Column(String, index=True)
    owner = Column(String, index=True)
    owner_id = Column(String, index=True)

    # owner_id = Column(Integer, ForeignKey("user.id"))
    # owner = relationship("User", back_populates="workflows")
