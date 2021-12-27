import { Workflow, WorkflowInfo, WorkflowInfoList } from '@app/_models';


export interface Job {
    id?: number;
    uuid: uuid
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;
    execute_at: Date;
    running: boolean;
    workflow: Workflow;
    workflow_type: string;
    workflow_execute_at: Date
    workflow_running: boolean;
}

export interface JobInfo {
    id?: number;
    uuid: uuid
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;
    execute_at: Date
    running: boolean;
    workflow_name: string;
    workflow_type: string;
    workflow_execute_at: Date
    workflow_running: boolean
}

export interface JobInfoList {
    data: JobInfo[];
}
