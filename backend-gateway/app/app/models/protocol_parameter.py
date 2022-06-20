from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.base_class import Base

if TYPE_CHECKING:
    pass


class ProtocolParameter(Base):
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, index=True)
    command_id = Column(Integer, ForeignKey('protocolcommand.id'))
    value = Column(String, index=False)