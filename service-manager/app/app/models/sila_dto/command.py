from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.sila_dto.command_parameter import CommandParameter
from app.models.sila_dto.command_responses import CommandResponse

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class Command(Base):
    __tablename__ = "commands"
    id = Column(Integer, primary_key=True, index=True)
    feature_id = Column(Integer, ForeignKey("feature.id"))
    feature = relationship("Feature", back_populates="features")
    identifier = Column(String(200))
    display_name = Column(String(200))
    observable = Column(Boolean)
    parameters = relationship("CommandParameter", order_by=CommandParameter.id, back_populates="commands")
    responses = relationship("CommandResponse", order_by=CommandResponse.id, back_populates="commands")
    error_identifiers = relationship("ErrorIdentifier", order_by=ErrorIdentifier.id, back_populates="commands")
