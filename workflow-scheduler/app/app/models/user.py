from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401
    from .job import Job # noqa: F401
    from .workflow import Workflow  # noqa: F401
    from .service import Service  # noqa: F401
    ######### Todo: Merge relict. Replace flow with workflow
    from .flow import Flow


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner")
    # jobs = relationship("Job", back_populates="owner")
    workflows = relationship("Workflow", back_populates="owner")

    ####### Todo: Merge relict. Replace flow with workflow
    # flows = relationship("Flow", back_populates="owner")
    #######

    services = relationship("Service", back_populates="owner")
