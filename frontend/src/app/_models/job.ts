import { Workflow, WorkflowInfo, WorkflowInfoList } from '@app/_models';


export interface Job {
    id?: number;
    uuid?: string;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;
    execute_at: Date;
    created_at: Date;
    running: boolean;
    workflow: Workflow;  // Do I ever need a Job class with the full workflow class inside?
    workflow_id?: number;
    workflow_type: string;
    workflow_execute_at: Date;
    workflow_running: boolean;
}

export interface JobInfo {
    id?: number;
    uuid?: string;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;
    execute_at: Date;
    created_at: Date;
    running: boolean;
    workflow_id: number;
    workflow_name: string;
    workflow_type: string;
    workflow_execute_at: Date;
    workflow_running: boolean;

    database_name: string;
}

export interface JobInfoList {
    data: JobInfo[];
}

export interface JobStatus {
    online: boolean;
    status: string;
}
