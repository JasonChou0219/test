from fastapi import APIRouter

from app import schemas

router = APIRouter()


@router.get("/features", response_model=schemas.Feature)
def get_features():
    print("Redirected")
    return {"Hello": "World"}
