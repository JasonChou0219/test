# Workflow Designer Python
-----------------------------

## Schemas for:

ScriptModel
class ScriptModel(BaseModel):
    name: str
    fileName: str
    data: str


ScriptInfoModel
class ScriptInfoModel(BaseModel):
    name: str
    fileName: str

## DB Models for
@dataclass
class ScriptInfo:
    id: int
    name: str
    fileName: str
    user: int


@dataclass
class Script:
    id: int
    name: str
    fileName: str
    user: int
    data: str


## Endpoints for:

Description:Get the information of a specific user-scripts
Frontend:
getUserWorkflowsInfo() -> WorkflowInfo[]:
@'/api/workflows_python'
Backend:
@app.get('/api/scripts/{scriptID}')
def get_user_script(scriptID: int, username: str = Depends(decode_token)):

-----------------------------------------------------
Description:Get the information of all registered user-scripts
getUserWorkflow(workflowID: number) -> Workflow:
@'/api/workflows_python/' + workflowID
Backend:
@app.get('/api/scripts')
def get_user_scripts_info(username: str = Depends(decode_token)):

-----------------------------------------------------
Description:
Frontend
setUserWorkflowInfo(workflowInfo: WorkflowInfo):
@`/api/workflows_python/${workflowInfo.id}/info`
Backend:
@app.put('/api/scripts/{scriptID}/info')
def set_user_script_info(scriptID: int,
                         info: ScriptInfoModel,):

-----------------------------------------------------
Description:
Frontend:
setUserWorkflow(workflow: Workflow):
@`/api/workflows_python/${workflow.id}/`, workflow
Backend:
@app.put('/api/scripts/{scriptID}/')
def set_user_script(scriptID: int,
                    script: ScriptModel,):

-----------------------------------------------------
Description:Add a new script object to the postgreSQL database
Frontend
createUserWorkflow(workflow: Workflow):
@'/api/workflows_python', workflow
Backend:
@app.post('/api/scripts')
def upload_user_script(script: ScriptModel,
                       username: str = Depends(decode_token)):
-----------------------------------------------------
Description: Delete a specific user-script from the postgreSQL database
Frontend:
deleteUserWorkflow(workflowID: number)
@'/api/workflows_python/' + workflowID
Backend:
@app.delete('/api/scripts/{scriptID}')
def delete_user_script(scriptID: int, username: str = Depends(decode_token)):




Dependency endpoints of feature

-----------------------------------------------------
getServiceList() -> Service[]:
@ '/api/services'

-----------------------------------------------------
getService(uuid: string) -> Service:
@'/api/services/' + uuid



