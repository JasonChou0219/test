from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.deps import get_db_workflow_designer as get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Flow])
def read_flows(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve flows.
    """
    if crud.user.is_superuser(current_user):
        flows = crud.flow.get_multi(db, skip=skip, limit=limit)
    else:
        flows = crud.flow.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return flows


@router.post("/", response_model=schemas.Flow)
def create_flow(
    *,
    db: Session = Depends(get_db),
    flow_in: schemas.FlowCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new flow.
    """
    flow = crud.flow.create_with_owner(db=db, obj_in=flow_in, owner_id=current_user.id)
    return flow


@router.put("/{uuid}", response_model=schemas.Flow)
def update_flow(
    *,
    db: Session = Depends(get_db),
    uuid: UUID,
    flow_in: schemas.FlowUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a flow.
    """
    flow = crud.flow.get(db=db, uuid=uuid)
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    if not crud.user.is_superuser(current_user) and (flow.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    flow = crud.flow.update(db=db, db_obj=flow, obj_in=flow_in)
    return flow


@router.get("/{id}", response_model=schemas.Flow)
def read_flow(
    *,
    db: Session = Depends(get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get flow by id.
    """
    flow = crud.flow.get(db=db, id=id)
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    if not crud.user.is_superuser(current_user) and (flow.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return flow


@router.delete("/{uuid}", response_model=schemas.Flow)
def delete_flow(
    *,
    db: Session = Depends(get_db),
    uuid: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a flow.
    """
    flow = crud.flow.get(db=db, uuid=uuid)
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    if not crud.user.is_superuser(current_user) and (flow.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    flow = crud.flow.remove(db=db, uuid=uuid)
    return flow
