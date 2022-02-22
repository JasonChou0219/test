from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi import Request

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Workflow])
def read_workflows(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve workflows.
    """
    query_params = dict(request.query_params.items())
    for key in ['skip', 'limit']:
        query_params.pop(key)
    user = schemas.User(**query_params)

    if user.is_superuser:
        workflows = crud.workflow.get_multi(db, skip=skip, limit=limit)
        print(workflows)
    else:
         workflows = crud.workflow.get_multi_by_owner(
             db=db, owner_id=user.id, skip=skip, limit=limit
         )
    return workflows


@router.post("/", response_model=schemas.Workflow)
def create_workflow(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        workflow_in: schemas.WorkflowCreate,
) -> Any:
    """
    Create new workflow.
    """
    user = schemas.User(**dict(request.query_params.items()))
    workflow_in.workflow_type = 'python'
    workflow = crud.workflow.create(db=db, obj_in=workflow_in)
    return workflow


@router.put("/{id}", response_model=schemas.Workflow)
def update_workflow(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
        workflow_in: schemas.WorkflowUpdate,
) -> Any:

    """
    Update an workflow.
    """
    query_params = dict(request.query_params.items())
    for key in ['id']:
        query_params.pop(key)
    user = schemas.User(**query_params)

    workflow = crud.workflow.get(db=db, id=id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if not user.is_superuser and (workflow.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    workflow = crud.workflow.update(db=db, db_obj=workflow, obj_in=workflow_in)
    return workflow


@router.get("/{id}", response_model=schemas.Workflow)
def read_workflow(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Get workflow by ID.
    """
    query_params = dict(request.query_params.items())
    # for key in ['id']:
    #     query_params.pop(key)
    user = schemas.User(**query_params)

    workflow = crud.workflow.get(db=db, id=id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if not user.is_superuser and (workflow.owner_id != user.id):
         raise HTTPException(status_code=400, detail="Not enough permissions")
    return workflow


@router.delete("/{id}", response_model=schemas.Workflow)
def delete_workflow(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Delete an workflow.
    """
    query_params = dict(request.query_params.items())
    for key in ['id']:
        query_params.pop(key)
    user = schemas.User(**query_params)

    workflow = crud.workflow.get(db=db, id=id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if not user.is_superuser and (workflow.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    workflow = crud.workflow.remove(db=db, id=id)
    return workflow
