from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from app.db.base_class import Base

if TYPE_CHECKING:
    from .flow import Flow  # noqa: F401


class Flow(Base):
    id = Column(String, primary_key=True, index=True)
    flow = Column(JSON)
    description = Column(String, index=True)
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="flows")
