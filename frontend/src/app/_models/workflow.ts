import { ServiceInfo } from '@app/_models';

export interface Workflow {
    id?: number;
    name: string;
    fileName: string;
    services?: ServiceInfo[];
    data: string;
    owner?: string;
    owner_id?: number;
    description?: string;
}
export interface WorkflowInfo {
    id?: number;
    name: string;
    fileName: string;
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
