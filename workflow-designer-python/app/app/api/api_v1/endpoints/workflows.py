from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Workflow])
def read_workflows(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: str = '',
) -> Any:
    """
    Retrieve workflows.
    """
    # if crud.user.is_superuser(current_user):
    if current_user == 'superuser':
        workflows = crud.workflow.get_multi(db, skip=skip, limit=limit)
        print(workflows)
    else:
         workflows = crud.workflow.get_multi_by_owner(
             db=db, owner_id=current_user, skip=skip, limit=limit
         )
    return workflows


@router.post("/", response_model=schemas.Workflow)
def create_workflow(
    *,
    db: Session = Depends(deps.get_db),
    workflow_in: schemas.WorkflowCreate,
) -> Any:
    """
    Create new workflow.
    """
    model = models.Workflow
    obj_in_data = jsonable_encoder(workflow_in)
    workflow = model(**obj_in_data)
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow


@router.put("/{id}", response_model=schemas.Workflow)
def update_workflow(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    workflow_in: schemas.WorkflowUpdate,
) -> Any:
    """
    Update an workflow.
    """
    workflow = crud.workflow.get(db=db, id=id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    # if not crud.user.is_superuser(current_user) and (workflow.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    workflow = crud.workflow.update(db=db, db_obj=workflow, obj_in=workflow_in)
    return workflow


@router.get("/{id}", response_model=schemas.Workflow)
def read_workflow(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get workflow by ID.
    """
    workflow = crud.workflow.get(db=db, id=id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    # if not crud.user.is_superuser(current_user) and (workflow.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    return workflow


@router.delete("/{id}", response_model=schemas.Workflow)
def delete_workflow(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: str = '',
) -> Any:
    """
    Delete an workflow.
    """
    workflow = crud.workflow.get(db=db, id=id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if current_user != 'superuser' and (workflow.owner_id != current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    workflow = crud.workflow.remove(db=db, id=id)
    return workflow
