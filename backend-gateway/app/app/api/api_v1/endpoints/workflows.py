from uuid import UUID

from requests import delete, get, post, put
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import parse_obj_as

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()
target_service_hostname = "http://sila2_manager_workflow-designer-python_1"  # -> to env var
target_service_port = settings.WORKFLOW_DESIGNER_PYTHON_UVICORN_PORT  # -> to env var
target_service_api_version = settings.API_V1_STR  # -> to env var

target_service_url_python = target_service_hostname + ":" \
                            + str(settings.WORKFLOW_DESIGNER_PYTHON_UVICORN_PORT) \
                            + str(settings.API_V1_STR) + "/workflows/"
target_service_url_node_red = "http://workflow-designer-node-red:85/flow-manager/all-flows/"


@router.get("/", response_model=List[schemas.Workflow])
def read_workflows(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    wf_type: str = "python",
    current_user: models.User = Depends(deps.get_current_active_user),  # get_current_active_superuser
) -> Any:
    """
    Retrieve workflows.
    """
    if wf_type == "python":
        target_route = target_service_url_python
    elif wf_type == "node-red":
        target_route = target_service_url_node_red
    if crud.user.is_superuser(current_user):
        print('abc')
        workflows = crud.workflow.get_multi(db, route=target_route, wf_type=wf_type, skip=skip, limit=limit, current_user=current_user)
    else:
        print('def')
        workflows = crud.workflow.get_multi_by_owner(
            db=db, route=target_route, current_user=current_user, skip=skip, limit=limit
        )
    return workflows


@router.post("/", response_model=schemas.Workflow)
def create_workflow(
    *,
    db: Session = Depends(deps.get_db),
    workflow_in: schemas.WorkflowCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new workflow.
    """
    print("### create_workflow ###")
    print(workflow_in)
    target_route = f"{target_service_url_python}"
    workflow_in.owner = current_user.email
    workflow_in.owner_id = current_user.id
    workflow = crud.workflow.create_with_owner(db=db, route=target_route, obj_in=workflow_in, current_user=current_user)
    workflow = parse_obj_as(schemas.WorkflowInDB, workflow.json())
    return workflow


@router.put("/{id}", response_model=schemas.Workflow)
def update_workflow(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    workflow_in: schemas.WorkflowUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a workflow.
    """
    target_route = f"{target_service_url_python}{id}"
    workflow = crud.workflow.get(db=db, route=target_route, id=id, current_user=current_user)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    else:
        workflow = parse_obj_as(schemas.WorkflowInDB, workflow.json())
        if not crud.user.is_superuser(current_user) and (workflow.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
    workflow = crud.workflow.update(db=db, route=target_route, db_obj=workflow,
                                    obj_in=workflow_in, current_user=current_user)
    workflow = parse_obj_as(schemas.WorkflowInDB, workflow.json())
    return workflow


@router.get("/{id}", response_model=schemas.Workflow)
def read_workflow(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get workflow by ID.
    """
    target_route = f"{target_service_url_python}{id}"
    workflow = crud.workflow.get(db=db, route=target_route, id=id, current_user=current_user)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    else:
        workflow = parse_obj_as(schemas.WorkflowInDB, workflow.json())
        if not crud.user.is_superuser(current_user) and (workflow.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
    return workflow


@router.delete("/{id}", response_model=schemas.Workflow)
def delete_workflow(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an workflow.
    """
    target_route = f"{target_service_url_python}{id}"
    workflow = crud.workflow.get(db=db, route=target_route, id=id, current_user=current_user)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    else:
        workflow = parse_obj_as(schemas.WorkflowInDB, workflow.json())
        if not crud.user.is_superuser(current_user) and (workflow.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
    workflow = crud.workflow.remove(db=db, route=target_route, id=id, current_user=current_user)
    workflow = parse_obj_as(schemas.WorkflowInDB, workflow.json())
    return workflow
