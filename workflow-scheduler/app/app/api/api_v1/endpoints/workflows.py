import json
from typing import Any, List
from uuid import UUID

from app.scheduler import container_logs
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
# from app.api.deps import get_db_workflow_designer_node_red as get_db_node_red
# from app.api.deps import get_db_workflow_designer_python as get_db_python
from starlette.websockets import WebSocketDisconnect
from websockets import ConnectionClosedOK, ConnectionClosedError

router = APIRouter()


@router.get("/", response_model=List[schemas.Workflow])
def read_workflows(
        db: Session = Depends(deps.get_db),
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
        db: Session = Depends(deps.get_db),
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
        db: Session = Depends(deps.get_db),
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
        db: Session = Depends(deps.get_db),
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
        db: Session = Depends(deps.get_db),
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


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        print('Disconnect')
        self.active_connections.remove(websocket)

    async def send_response(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/logs/{job_uuid}_{workflow_uuid}")
async def logs_websocket(websocket: WebSocket, job_uuid: str, workflow_uuid: str):
    """
    Get the logs of a workflow.
    """
    await manager.connect(websocket)
    try:
        # await manager.send_response(json.dumps({f'{job_uuid}_{workflow_uuid}':
        #                                         container_logs[job_uuid][workflow_uuid]['log_buffer'].queue}),
        #                             websocket)
        await manager.send_response(str({f'{job_uuid}_{workflow_uuid}': container_logs}),
                                    websocket)

        for line in container_logs[int(job_uuid)][int(workflow_uuid)]['log_stream']:
            print(line, flush=True)
            await manager.send_response(json.dumps({f'{job_uuid}_{workflow_uuid}': line.decode()}),
                                        websocket)
    except KeyError:
        raise HTTPException(status_code=404, detail="No entry found with Job/Workflow ID combination.")
    except (WebSocketDisconnect, ConnectionClosedOK, ConnectionClosedError):
        manager.disconnect(websocket)
