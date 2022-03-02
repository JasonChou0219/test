from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Request

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Protocol])
def read_protocols(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve protocols.
    """
    query_params = dict(request.query_params.items())
    for key in ['skip', 'limit']:
        query_params.pop(key)
    user = models.User(**query_params)

    if user.is_superuser:
        protocols = crud.protocol.get_multi(db, skip=skip, limit=limit)
    else:
        protocols = crud.protocol.get_multi_by_owner(
            db=db, owner_id=user.id, skip=skip, limit=limit
        )
    protocols_as_schema = []
    for protocol in protocols:
        protocols_as_schema.append(protocol_schema_from_model(protocol))
    return protocols_as_schema


@router.post("/", response_model=schemas.Protocol)
def create_protocol(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        protocol_in: schemas.ProtocolCreate,
) -> Any:
    """
    Create new protocol.
    """
    query_params = dict(request.query_params.items())
    user = models.User(**query_params)

    protocol_in.owner_id = user.id
    protocol_in.owner = user.email

    protocol = protocol_model_from_schema_create(protocol_in)

    db.add(protocol)
    db.commit()
    db.refresh(protocol)

    return protocol_schema_from_model(protocol)


@router.put("/{id}", response_model=schemas.Protocol)
def update_protocol(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
        protocol_in: schemas.ProtocolCreate,
) -> Any:
    """
    Update a protocol.
    """
    query_params = dict(request.query_params.items())
    user = models.User(**query_params)

    protocol = crud.protocol.get(db=db, id=id)
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")
    if not user.is_superuser and (protocol.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    protocol_in.owner_id = user.id
    protocol_in.owner = user.email

    protocol = crud.protocol.update(db=db, db_obj=protocol, obj_in=protocol_in)

    setattr(protocol, "service", protocol_model_from_schema_update(protocol_in).service)

    db.add(protocol)
    db.commit()
    db.refresh(protocol)

    return protocol_schema_from_model(protocol)


@router.get("/{id}", response_model=schemas.Protocol)
def read_protocol(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Get protocol by ID.
    """
    query_params = dict(request.query_params.items())
    user = models.User(**query_params)

    protocol = crud.protocol.get(db=db, id=id)
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")
    if not user.is_superuser and (protocol.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return protocol_schema_from_model(protocol)


@router.delete("/{id}", response_model=schemas.Protocol)
def delete_protocol(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Delete a protocol.
    """
    query_params = dict(request.query_params.items())
    user = models.User(**query_params)

    protocol = crud.protocol.get(db=db, id=id)
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")
    if not user.is_superuser and (protocol.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    protocol = crud.protocol.remove(db=db, id=id)
    return protocol_schema_from_model(protocol)


def protocol_model_from_schema_create(protocol_in: schemas.ProtocolCreate) -> models.Protocol:
    protocol = models.Protocol(title=protocol_in.title,
                               owner_id=protocol_in.owner_id,
                               owner=protocol_in.owner)
    service = models.Service(uuid=protocol_in.service.uuid)
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


def protocol_model_from_schema_update(protocol_in: schemas.ProtocolUpdate) -> models.Protocol:
    protocol = models.Protocol(title=protocol_in.title,
                               owner_id=protocol_in.owner_id,
                               owner=protocol_in.owner)
    service = models.Service(uuid=protocol_in.service.uuid)
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


def protocol_schema_from_model(protocol_in: models.Protocol) -> schemas.Protocol:
    features = []
    for feature_in in protocol_in.service.features:
        commands = []
        properties = []
        for command_in in feature_in.commands:
            parameters = []
            responses = []
            for parameter_in in command_in.parameters:
                parameter = schemas.Parameter(id=parameter_in.id,
                                              identifier=parameter_in.identifier,
                                              value=parameter_in.value)
                parameters.append(parameter)
            for response_in in command_in.responses:
                response = schemas.Response(id=response_in.id,
                                            identifier=response_in.identifier)
                responses.append(response)
            command = schemas.Command(id=command_in.id,
                                      identifier=command_in.identifier,
                                      observable=command_in.observable,
                                      meta=command_in.meta,
                                      interval=command_in.interval,
                                      parameters=parameters,
                                      responses=responses)
            commands.append(command)
        for property_in in feature_in.properties:
            property = schemas.Property(id=property_in.id,
                                        identifier=property_in.identifier,
                                        observable=property_in.observable,
                                        meta=property_in.meta,
                                        interval=property_in.interval)
            properties.append(property)
        feature = schemas.Feature(id=feature_in.id,
                                  identifier=feature_in.identifier,
                                  commands=commands,
                                  properties=properties)
        features.append(feature)

    service = schemas.Service(id=protocol_in.service.id,
                              uuid=protocol_in.service.uuid,
                              features=features)

    protocol = schemas.Protocol(id=protocol_in.id,
                                title=protocol_in.title,
                                owner_id=protocol_in.owner_id,
                                owner=protocol_in.owner,
                                service=service)

    return protocol


def check_protocol(protocol: models.Protocol, user: models.User):
    pass
