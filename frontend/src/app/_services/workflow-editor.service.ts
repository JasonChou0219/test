import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { env } from '@environments/environment';

import { Workflow, WorkflowInfo, WorkflowInfoList } from '@app/_models';

@Injectable({
    providedIn: 'root',
})
export class WorkflowEditorService {
    // serverUrl = env.backendHttpUrl;
    serverUrl = env.apiUrl;
    constructor(private http: HttpClient) {
    }

    async getUserWorkflowsInfo(): Promise<WorkflowInfo[]> {
        return this.http
            .get<WorkflowInfo[]>(`${env.apiUrl}/api/v1/workflows/`)
            .pipe(map((workflow) => workflow))
            .toPromise();
    }
    async getUserWorkflow(workflowID: number): Promise<Workflow> {
        return this.http
            .get<Workflow>(`${env.apiUrl}/api/v1/workflows/` + workflowID)
            .toPromise();
    }
    async setUserWorkflowInfo(workflowInfo: WorkflowInfo) {
        return this.http
            .put(
                `${env.apiUrl}/api/v1/workflows/${workflowInfo.id}/info`,
                workflowInfo
            )
            .toPromise();
    }
    async setUserWorkflow(workflow: Workflow) {
        return this.http
            .put(`${env.apiUrl}/api/v1/workflows/${workflow.id}/`, workflow)
            .toPromise();
    }
    async createUserWorkflow(workflow: Workflow) {
        return this.http
            .post('${env.apiUrl}/api/v1/workflows', workflow)
            .toPromise();
    }
    async deleteUserWorkflow(workflowID: number) {
        return this.http
            .delete('${env.apiUrl}/api/v1/workflows/' + workflowID)
            .toPromise();
    }
}
