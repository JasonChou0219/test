from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class DataType(Base):
    __tablename__="datatypes"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(200))
