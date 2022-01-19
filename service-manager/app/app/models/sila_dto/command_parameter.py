from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class CommandParameter(Base):
    __tablename__ = "command_parameters"
    id = Column(Integer, primary_key=True, index=True)
    command_id = Column(Integer, ForeignKey("command.id"))
    identifier = Column(String(200))
    display_name = Column(String(200))
    description = Column(String(200))
    data_type_id = Column(Integer, ForeignKey("datatype.id"))
    data_type = relationship("DataType", back_populates="command_parameters")
