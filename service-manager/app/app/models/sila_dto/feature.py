from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from .command import Command
from .error import DefinedExecutionError
from .property import Property

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class Feature(Base):
    __tablename__="features"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(200))
    feature_version = Column(String(200))
    maturity_level = Column(String(200))
    originator = Column(String(200))
    sila2_version = Column(String(200))
    identifier = Column(String(200), index=True)
    display_name = Column(String(200))
    description = Column(String(200))
    locale = Column(String(200))
    commands = relationship("Command", order_by=Command.id, back_populates="features")
    properties = relationship("Property", order_by=Property.id, back_populates="features")
    errors = relationship("Error", order_by=DefinedExecutionError.id, back_populates="features")
