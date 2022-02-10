from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.feature import Feature

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class ServiceInfo(Base):
    __tablename__ = "service_info"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(200))
    parsed_ip_address = Column(String(200))
    port = Column(String(200))
    uuid = Column(String(200))
    version = Column(String(200))
    server_name = Column(String(200), index=True)
    description = Column(String(200))
    favourite = Column(Boolean)
    feature_names = relationship("Feature", order_by=Feature.id, back_populates="service_info")
