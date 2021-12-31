import {
    Workflow, WorkflowInfoList,
    Dataflow, DataflowInfoList,
    DataProtocol, DataProtocolInfoList,
} from '@app/_models';


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
    workflows?: Workflow[];
    dataflows?: Dataflow[];
    data_protocols?: DataProtocol[];
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
    workflows?: WorkflowInfoList;
    dataflows?: DataflowInfoList;
    data_protocols?: DataProtocolInfoList;
}

export interface JobInfoList {
    data: JobInfo[];
}

export interface JobStatus {
    online: boolean;
    status: string;
}
