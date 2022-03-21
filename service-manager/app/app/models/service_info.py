from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Boolean

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class ServiceInfo(Base):
    __tablename__ = "service_info"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    type = Column(String(200))
    parsed_ip_address = Column(String(200))
    port = Column(String(200))
    uuid = Column(String(200), unique=True, index=True)
    version = Column(String(200))
    server_name = Column(String(200), index=True)
    description = Column(String(200))
    favourite = Column(Boolean)
    isGateway = Column(Boolean)
    feature_names = Column(String)
    owner_id = Column(Integer)
    owner = Column(String(200))
