import { ServiceInfo } from '@app/_models';

export interface Workflow {
    id?: number;
    title: string;
    fileName: string;
    services?: ServiceInfo[];
    workflow_type: string;
    data: string;
    owner?: string;
    owner_id?: number;
    description?: string;
}
export interface WorkflowInfo {
    id?: number;
    title: string;
    fileName: string;
    workflow_type: string;
    services?: ServiceInfo[];
    data: string;
    owner?: string;
    owner_id?: number;
    description?: string;
}

export interface WorkflowInfoList {
    // data: WorkflowInfo[];
    data: WorkflowInfo[];
}
