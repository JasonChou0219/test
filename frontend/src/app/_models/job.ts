import {
    Workflow, WorkflowInfoList, WorkflowInfoTuple,
    Dataflow, DataflowInfoList,
    DataProtocol, DataProtocolInfoList,
    Protocol, Database,
} from '@app/_models';


export interface Job {
    id?: number;
    // uuid?: string;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;

    workflows?: Workflow[];
    dataflows?: Dataflow[];
    // data_protocols?: DataProtocol[];
    list_protocol_and_database?: ProtocolAndDatabaseTuple[];

    execute_at: Date;
    created_at: Date;
    running: boolean;
    database: string;
}

export interface JobInfo {
    id?: number;
    // uuid?: string;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;

    workflows?: WorkflowInfoTuple[];  // WorkflowInfoList[];
    dataflows?: DataflowInfoList;
    // data_protocols?: DataProtocolInfoList;
    list_protocol_and_database?: [number, number][];

    execute_at: Date;
    created_at: Date;
    running: boolean;
    database?: string;
}

export interface JobInfoList {
    data: JobInfo[];
}

export interface JobStatus {
    online: boolean;
    status: string;
}

export interface ProtocolAndDatabaseTuple {
    protocol: Protocol;
    database: Database;
}
