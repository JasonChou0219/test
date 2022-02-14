from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
# from app.api.deps import get_db_workflow_designer_node_red as get_db_node_red
# from app.api.deps import get_db_workflow_designer_python as get_db_python

router = APIRouter()


@router.get("/", response_model=List[schemas.Workflow])
def read_workflows(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve flows.
    """
    if crud.user.is_superuser(current_user):
        workflows = crud.workflow.get_multi(db, skip=skip, limit=limit)
    else:
        workflows = crud.workflow.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return workflows


@router.post("/", response_model=schemas.Workflow)
def create_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_in: schemas.WorkflowCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new workflow.
    """
    workflow = crud.workflow.create_with_owner(db=db, obj_in=workflow_in, owner_id=current_user.id)
    return workflow


@router.put("/{uuid}", response_model=schemas.Workflow)
def update_workflow(
    *,
    db: Session = Depends(get_db),
    uuid: UUID,
    workflow_in: schemas.WorkflowUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a workflow.
    """
    workflow = crud.workflow.get(db=db, uuid=uuid)

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if not crud.user.is_superuser(current_user) and (workflow.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    workflow = crud.workflow.update(db=db, db_obj=workflow, obj_in=workflow_in)
    return workflow


@router.get("/{workflow_type}_{uuid}", response_model=schemas.Workflow)
def read_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_type: str,
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get workflow by id.
    """

    workflow = crud.workflow.get(db=db, uuid=uuid)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if not crud.user.is_superuser(current_user) and (workflow.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return workflow


@router.delete("/{uuid}", response_model=schemas.Workflow)
def delete_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_type: str,
    uuid: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a workflow.
    """
    workflow = crud.workflow.get(db=db, uuid=uuid)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if not crud.user.is_superuser(current_user) and (workflow.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    workflow = crud.workflow.remove(db=db, uuid=uuid)
    return workflow
