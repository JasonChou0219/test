from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from app.db.base_class import Base
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    pass


class Command(Base):
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, index=True)
    observable = Column(Boolean, index=False)
    meta = Column(Boolean, index=False)
    interval = Column(Integer, index=False)
    feature_id = Column(Integer, ForeignKey('feature.id'))
    parameters = relationship("Parameter", cascade="all, delete-orphan", lazy='joined')
    responses = relationship("Response", cascade="all, delete-orphan", lazy='joined')
