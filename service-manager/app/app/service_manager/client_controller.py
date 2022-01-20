from multiprocessing.pool import ThreadPool
from typing import List

from sila2.client import SilaClient

from app.schemas.sila_dto import Feature


class FeatureController:
    silaClient: SilaClient
    features: List[Feature]
