from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class DefinedExecutionError(Base):
    __tablename__ = "errors"
    id = Column(Integer, primary_key=True, index=True)
    feature_id = Column(Integer, ForeignKey('feature.id'))
    identifier = Column(String(200))
    display_name = Column(String(200))
    description = Column(String(200))
