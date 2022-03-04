from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from requests import get
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

    check_protocol(protocol_in, user)

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

    check_protocol(protocol_in, user)

    # TODO do not allow to modify service?

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
    user_dict = jsonable_encoder(user)
    response = get("http://service-manager:82/api/v1/sm_functions/browse_features", params=dict({'service_uuid': protocol.service.uuid}, **user_dict))

    # TODO check no duplicate features, commands, parameters, etc. exist
    # TODO check interval value

    if not response:
        raise HTTPException(status_code=response.status_code,
                            detail=response.json()['detail'],
                            headers=response.headers)

    # Retrieve features information from response
    actual_features = {}
    for feature in jsonable_encoder(response.json()):
        actual_features[feature['identifier']] = {}

        actual_commands = {}
        for command in feature['commands']:
            actual_command = {'observable': command['observable'],
                              'parameters': [],
                              'responses': []}
            for parameter in command['parameters']:
                actual_command['parameters'].append(parameter['identifier'])
            for response in command['responses']:
                actual_command['responses'].append(response['identifier'])
            actual_commands[command['identifier']] = actual_command
        actual_features[feature['identifier']]['commands'] = actual_commands

        actual_properties = {}
        for property in feature['properties']:
            actual_property = {'observable': property['observable']}
            actual_properties[property['identifier']] = actual_property
        actual_features[feature['identifier']]['properties'] = actual_properties

    # Check protocol information actually exists for specified service

    # Check features exist
    for protocol_feature in protocol.service.features:
        if protocol_feature.identifier not in actual_features.keys():
            raise HTTPException(status_code=404,
                                detail=("Feature " + protocol_feature.identifier
                                        + " does not exist for service " + protocol.service.uuid))

        # Check commands exist
        for protocol_command in protocol_feature.commands:
            if protocol_command.identifier not in actual_features[protocol_feature.identifier]['commands'].keys():
                raise HTTPException(status_code=404,
                                    detail=("Command " + protocol_command.identifier
                                            + " does not exist for feature " + protocol_feature.identifier
                                            + " for service " + protocol.service.uuid))

            # Check command observable property is the same
            if protocol_command.observable != actual_features[protocol_feature.identifier]['commands'][protocol_command.identifier]['observable']:
                raise HTTPException(status_code=405,
                                    detail=("Command " + protocol_command.identifier
                                            + " for feature " + protocol_feature.identifier
                                            + " for service " + protocol.service.uuid
                                            + " has observable value of " + str(actual_features[protocol_feature.identifier]['commands'][protocol_command.identifier]['observable'])))

            # Check parameters exist
            for protocol_parameter in protocol_command.parameters:
                if protocol_parameter.identifier not in actual_features[protocol_feature.identifier]['commands'][protocol_command.identifier]['parameters']:
                    raise HTTPException(status_code=404,
                                        detail=("Parameter " + protocol_parameter.identifier
                                                + " does not exist for command " + protocol_command.identifier
                                                + " for feature " + protocol_feature.identifier
                                                + " for service " + protocol.service.uuid))

            # Check all parameters are specified
            protocol_parameters_identifiers = [protocol_parameter.identifier for protocol_parameter in protocol_command.parameters]
            for required_parameter in actual_features[protocol_feature.identifier]['commands'][protocol_command.identifier]['parameters']:
                if required_parameter not in protocol_parameters_identifiers:
                    raise HTTPException(status_code=404,
                                        detail=("Parameter " + required_parameter
                                                + " is not provided for command " + protocol_command.identifier
                                                + " for feature " + protocol_feature.identifier
                                                + " for service " + protocol.service.uuid))

            # If no responses are specified, add all of them
            if not protocol_command.responses:
                for response in actual_features[protocol_feature.identifier]['commands'][protocol_command.identifier]['responses']:
                    protocol_command.responses.append(models.Response(identifier=response))
            # Otherwise check that the specified responses exist
            else:
                for protocol_response in protocol_command.responses:
                    if protocol_response.identifier not in actual_features[protocol_feature.identifier]['commands'][protocol_command.identifier]['responses']:
                        raise HTTPException(status_code=404,
                                            detail=("Response " + protocol_response.identifier
                                                    + " does not exist for command " + protocol_command.identifier
                                                    + " for feature " + protocol_feature.identifier
                                                    + " for service " + protocol.service.uuid))

        # Check properties exist
        for protocol_property in protocol_feature.properties:
            if protocol_property.identifier not in actual_features[protocol_feature.identifier]['properties'].keys():
                raise HTTPException(status_code=404,
                                    detail=("Property " + protocol_property.identifier
                                            + " does not exist for feature " + protocol_feature.identifier
                                            + " for service " + protocol.service.uuid))

            # Check property observable property is the same
            if protocol_property.observable != actual_features[protocol_feature.identifier]['properties'][protocol_property.identifier]['observable']:
                raise HTTPException(status_code=405,
                                    detail=("Property " + protocol_property.identifier
                                            + " for feature " + protocol_feature.identifier
                                            + " for service " + protocol.service.uuid
                                            + " has observable value of " + str(actual_features[protocol_feature.identifier]['properties'][protocol_property.identifier]['observable'])))
