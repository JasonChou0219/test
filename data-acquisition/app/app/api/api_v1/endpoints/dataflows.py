from requests import get
from typing import Any, List

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[dict])
def read_dataflows(
) -> Any:
    """
    Retrieve dataflows.
    """
    url = "https://" + settings.KNIME_SERVER_HOST + ":" + str(settings.KNIME_SERVER_PORT) \
          + "/knime/rest/v4/repository/?deep=true"
    response = get(
        url, auth=(settings.KNIME_SERVER_USER, settings.KNIME_SERVER_PASSWORD),
        verify=False
    ).json()

    # Workflow groups are also included in the response, so we need to go through the tree and extract the workflows
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
            dataflow['owner'] = node['owner']
            dataflows.append(dataflow)
    return dataflows
