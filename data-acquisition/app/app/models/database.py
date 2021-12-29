from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String

from app.db.base_class import Base

if TYPE_CHECKING:
    pass


class Database(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String, index=False)
    password = Column(String, index=False)
    address = Column(String, index=False)
    port = Column(Integer, index=False)
    owner = Column(String, index=True)
    owner_id = Column(String, index=True)
