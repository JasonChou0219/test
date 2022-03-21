from typing import Any, Dict

from sqlalchemy.orm import Session

from app import models, schemas
from app.crud.base import CRUDBase
from app.models import ServiceInfo
from app.schemas import ServiceInfoCreate, ServiceInfoUpdate


class CRUDServiceInfo(CRUDBase[ServiceInfo, ServiceInfoCreate, ServiceInfoUpdate]):

    def get_service_info(self, db: Session, service_info_id: int):
        return db.query(models.ServiceInfo).filter(models.ServiceInfo.id == service_info_id).first()

    def get_service_info_by_server_uuid(self, db: Session, uuid: str):
        yield db.query(models.ServiceInfo).filter(models.ServiceInfo.uuid == uuid).first()

    def has_service_info_by_server_uuid(self, db: Session, uuid: str):
        yield db.query(models.ServiceInfo).filter(models.ServiceInfo.uuid == uuid).first()

    def get_all_service_info(self, db: Session):
        return db.query(models.ServiceInfo).all()

    def create_service_info(self, db: Session, service_info: schemas.ServiceInfoCreate, owner_id: int, owner: str):
        db_service_info = models.ServiceInfo(**service_info.dict())
        db.add(db_service_info)
        db.commit()
        db.refresh(db_service_info)
        return db_service_info

    def update_service_info(self, db: Session, uuid: str, data: Dict[str, Any]):
        db.query(models.ServiceInfo).filter(models.ServiceInfo.uuid == uuid).update(data)
        db.commit()
        return True

    def delete_service_info(self, db: Session, uuid: str):
        db.query(models.ServiceInfo).filter(models.ServiceInfo.uuid == uuid).delete()
        db.commit()
        return True


service_info = CRUDServiceInfo(ServiceInfo)
