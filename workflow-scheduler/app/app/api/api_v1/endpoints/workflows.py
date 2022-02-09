from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.deps import get_db_workflow_designer_node_red as get_db_node_red
from app.api.deps import get_db_workflow_designer_python as get_db_python

router = APIRouter()


@router.get("/", response_model=List[schemas.Workflow])
def read_workflows(
    db_node_red: Session = Depends(get_db_node_red),
    db_python: Session = Depends(get_db_node_red),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve flows.
    """
    if crud.user.is_superuser(current_user):
        workflows_node_red = crud.workflow.get_multi(db_node_red, skip=skip, limit=limit)
        workflows_python = crud.workflow.get_multi(db_python, skip=skip, limit=limit)
    else:
        workflows_node_red = crud.workflow.get_multi_by_owner(
            db=db_node_red, owner_id=current_user.id, skip=skip, limit=limit
        )
        workflows_python = crud.workflow.get_multi_by_owner(
            db=db_python, owner_id=current_user.id, skip=skip, limit=limit
        )
    workflows = dict(workflows_node_red, **workflows_python)
    return workflows


@router.post("/", response_model=schemas.Workflow)
def create_workflow(
    *,
    db_node_red: Session = Depends(get_db_node_red),
    db_python: Session = Depends(get_db_node_red),
    workflow_in: schemas.WorkflowCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new workflow.
    """
    if workflow_in.workflow_type == 'node-red':
        workflow = crud.workflow.create_with_owner(db=db_node_red, obj_in=workflow_in, owner_id=current_user.id)
    elif workflow_in.workflow_type == 'python':
        workflow = crud.workflow.create_with_owner(db=db_python, obj_in=workflow_in, owner_id=current_user.id)
    else:
        workflow = crud.workflow.create_with_owner(db=db_python, obj_in=workflow_in, owner_id=current_user.id)
        pass
        # Todo: Implement a reasonable default or raise an exception
    return workflow


@router.put("/{uuid}", response_model=schemas.Workflow)
def update_workflow(
    *,
    db_node_red: Session = Depends(get_db_node_red),
    db_python: Session = Depends(get_db_node_red),
    uuid: UUID,
    workflow_in: schemas.WorkflowUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a workflow.
    """
    if workflow_in.workflow_type == 'node-red':
        workflow = crud.workflow.get(db=db_node_red, uuid=uuid)
        db = db_node_red
    elif workflow_in.workflow_type == 'python':
        workflow = crud.workflow.get(db=db_python, uuid=uuid)
        db = db_python
    else:
        workflow = crud.workflow.get(db=db_python, uuid=uuid)
        db = db_python
        # Todo: Implement a reasonable default or raise an exception

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if not crud.user.is_superuser(current_user) and (workflow.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    workflow = crud.workflow.update(db=db, db_obj=workflow, obj_in=workflow_in)
    return workflow


@router.get("/{workflow_type}_{uuid}", response_model=schemas.Workflow)
def read_workflow(
    *,
    db_node_red: Session = Depends(get_db_node_red),
    db_python: Session = Depends(get_db_node_red),
    workflow_type: str,
    uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get workflow by id.
    """
    if workflow_type == 'node-red':
        workflow = crud.workflow.get(db=db_node_red, uuid=uuid)
    elif workflow_type == 'python':
        workflow = crud.workflow.get(db=db_python, uuid=uuid)
    else:
        workflow = crud.workflow.get(db=db_python, uuid=uuid)
        # Todo: Implement a reasonable default or raise an exception
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if not crud.user.is_superuser(current_user) and (workflow.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return workflow


@router.delete("/{uuid}", response_model=schemas.Workflow)
def delete_workflow(
    *,
    db_node_red: Session = Depends(get_db_node_red),
    db_python: Session = Depends(get_db_node_red),
    workflow_type: str,
    uuid: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a workflow.
    """
    if workflow_type == 'node-red':
        workflow = crud.workflow.get(db=db_node_red, uuid=uuid)
        db = db_node_red
    elif workflow_type == 'python':
        workflow = crud.workflow.get(db=db_python, uuid=uuid)
        db = db_python
    else:
        workflow = crud.workflow.get(db=db_python, uuid=uuid)
        db = db_python
        # Todo: Implement a reasonable default or raise an exception
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if not crud.user.is_superuser(current_user) and (workflow.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    workflow = crud.workflow.remove(db=db, uuid=uuid)
    return workflow
