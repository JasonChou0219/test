from sqlalchemy.orm import Session

from app import models, schemas
from app.crud.base import CRUDBase
from app.models import Feature
from app.schemas import SilaFeatureCreate, SilaFeatureUpdate


class CRUDFeatureInfo(CRUDBase[Feature, SilaFeatureCreate, SilaFeatureUpdate]):

    def create_feature_for_uuid(self, db: Session, feature: SilaFeatureCreate):
        db_feature = models.Feature(**feature.dict())
        db.add(db_feature)
        db.commit()
        db.refresh(db_feature)
        return db_feature

    def get_all_features_for_uuid(self, db: Session, service_info_uuid: str):
        return db.query(models.Feature).filter(models.Feature.owner_uuid == service_info_uuid).all()

    def remove_all_features_for_uuid(self, db: Session, service_info_uuid: str):
        db.query(models.Feature).filter(models.Feature.owner_uuid == service_info_uuid).delete()
        db.commit()
        return True


feature = CRUDFeatureInfo(Feature)
