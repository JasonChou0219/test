from requests import delete, get, post, put
from typing import Any, List
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.api.deps import get_db_workflow_designer_node_red

router = APIRouter()
workflow_designer_python_hostname = "http://sila2_manager_workflow-designer-python_1"  # -> to env var
workflow_designer_python_service_url = workflow_designer_python_hostname + ":" \
                     + str(settings.WORKFLOW_DESIGNER_PYTHON_UVICORN_PORT) \
                     + str(settings.API_V1_STR) + "/"

data_acquisition_hostname = "http://sila2_manager_data-acquisition_1"  # -> to env var
data_acquisition_service_url = data_acquisition_hostname + ":" \
                               + str(settings.DATA_ACQUISITION_UVICORN_PORT) \
                               + str(settings.API_V1_STR) + "/"


@router.get("/", response_model=List[schemas.Job])
def read_jobs(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve jobs.
    """
    query_params = dict(request.query_params.items())
    for key in ['skip', 'limit']:
        query_params.pop(key)
    user = schemas.User(**query_params)

    if user.is_superuser:
        jobs = crud.job.get_multi(db, skip=skip, limit=limit)
    else:
        jobs = crud.job.get_multi_by_owner(
            db=db, owner_id=user.id, skip=skip, limit=limit
        )
    return jobs


@router.post("/", response_model=schemas.Job)
def create_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        job_in: schemas.JobCreate,
) -> Any:
    """
    Create new job.
    """
    user = schemas.User(**dict(request.query_params.items()))
    user_dict = jsonable_encoder(user)
    job_in.owner = user.email
    job_in.owner_id = user.id
    job_in.created_at = datetime.now()

    workflows: List = []
    for workflow in job_in.workflows:
        print(workflow)
        if workflow[1] == 'python':
            print('This is a python workflow')
            workflow = get(f"{workflow_designer_python_service_url}workflows/{workflow[0]}",
                           params=dict(**user_dict))
            workflows.append(workflow)
        elif workflow[1] == 'node-red':
            # Todo: Change this from a database call (MS-Architecture ffs!) to a request --> implement a respective
            #  endpoint in the workflow-designer-node-red
            # Todo: Add workfow_type = "node-red" to the workflow object stored in the workflow-designer-node-red
            #  database --> Use the  same model and schema that we use here!
            print('This is a node-red workflow')
            db_designer = get_db_workflow_designer_node_red()
            _ = next(db_designer)
            # Retrieve flow with specified ID
            workflow = crud.workflow.get(db=_, id=workflow[0])
            workflows.append(workflow)
    try:
        job = crud.job.create(db=db, obj_in=job_in)
        for workflow in workflows:
            crud.workflow.create_with_owner(db=db, obj_in=workflow, owner_id=job.id)
        for index in range(len(job_in.list_protocol_and_database)):
            protocol = job_in.list_protocol_and_database[index][0]
            database = job_in.list_protocol_and_database[index][1]

            protocol = get(f"{data_acquisition_service_url}protocols/{protocol}",
                           params=dict(**user_dict))
            database = get(f"{data_acquisition_service_url}databases/{database}",
                           params=dict(**user_dict))

            protocol_model = protocol_model_from_schema(schemas.Protocol.parse_obj(protocol.json()))
            protocol_model.job_id = job.id
            db.add(protocol_model)
            db.commit()
            db.refresh(protocol_model)

            database = crud.database.create_with_owner(db=db, obj_in=database, owner_id=job.id)

            job_in.list_protocol_and_database[index] = (protocol_model.id, database.id)
        job = crud.job.get(db=db, id=job.id)
        job = crud.job.update(db=db, db_obj=job, obj_in=job_in)
    except IntegrityError as db_exception:
        raise HTTPException(status_code=452, detail=f"{type(db_exception).__name__}:{db_exception.orig}")
    return job


@router.put("/{id}", response_model=schemas.Job)
def update_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
        job_in: schemas.JobUpdate,
) -> Any:
    """
    Update a job.
    """
    query_params = dict(request.query_params.items())
    for key in ['id']:
        query_params.pop(key)
    user = schemas.User(**query_params)

    job = crud.job.get(db=db, id=id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not user.is_superuser and (job.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    job = crud.job.update(db=db, db_obj=job, obj_in=job_in)
    return job


@router.get("/{id}", response_model=schemas.Job)
def read_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Get job by UUID.
    """
    query_params = dict(request.query_params.items())
    print(query_params)
    for key in ['id']:
        query_params.pop(key)
    user = schemas.User(**query_params)

    job = crud.job.get(db=db, id=id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not user.is_superuser and (job.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return job


@router.delete("/{id}", response_model=schemas.Job)
def delete_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Delete a job.
    """
    query_params = dict(request.query_params.items())
    print(query_params)
    for key in ['id']:
        query_params.pop(key)
    user = schemas.User(**query_params)
    print(user)
    print(user.full_name)
    print(type(user.id))
    job = crud.job.get(db=db, id=id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not user.is_superuser != 'superuser' and (job.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    job = crud.job.remove(db=db, id=id)
    return job


# This is necessary because the conversion schema<->model does not work for nested objects
def protocol_model_from_schema(protocol_in: schemas.Protocol) -> models.Protocol:
    protocol = models.Protocol(title=protocol_in.title,
                               custom_data=protocol_in.custom_data,
                               owner_id=protocol_in.owner_id,
                               owner=protocol_in.owner)
    service = models.ProtocolService(uuid=protocol_in.service.uuid)
    features = []
    for feature_in in protocol_in.service.features:
        feature = models.Feature(identifier=feature_in.identifier)
        commands = []
        properties = []
        for command_in in feature_in.commands:
            command = models.Command(identifier=command_in.identifier,
                                     observable=command_in.observable,
                                     meta=command_in.meta,
                                     interval=command_in.interval)
            parameters = []
            responses = []
            for parameter_in in command_in.parameters:
                parameter = models.Parameter(identifier=parameter_in.identifier,
                                             value=parameter_in.value)
                parameters.append(parameter)
            for response_in in command_in.responses:
                response = models.Response(identifier=response_in.identifier)
                responses.append(response)
            command.parameters = parameters
            command.responses = responses
            commands.append(command)
        for property_in in feature_in.properties:
            property = models.Property(identifier=property_in.identifier,
                                       observable=property_in.observable,
                                       meta=property_in.meta,
                                       interval=property_in.interval)
            properties.append(property)
        feature.commands = commands
        feature.properties = properties
        features.append(feature)
    service.features = features
    protocol.service = service

    return protocol
