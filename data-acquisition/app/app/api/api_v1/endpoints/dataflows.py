from requests import delete, get, post, put
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[dict])
def read_dataflows(
) -> Any:
    """
    Retrieve dataflows.
    """
    response = get(
        "https://10.152.248.14:8443/knime/rest/v4/repository/?deep=true", auth=('knimeadmin', 'diginbio-server'),
        verify=False
    ).json()

    # Workflow groups are also included in the response, so we need to extract the workflows
    response_items = [response]
    dataflows = []
    while response_items:
        node = response_items.pop()
        if 'children' in node.keys():
            response_items.extend(node['children'])
        if node['type'] == 'Workflow':
            dataflow = {}
            dataflow['path'] = node['path']
            dataflow['created_on'] = node['createdOn']
            dataflow['last_edited_on'] = node['lastEditedOn']
            dataflow['openapi_link'] = node['@controls']['self']['href'] + ':openapi?showInUI=true'
            dataflows.append(dataflow)
    return dataflows
