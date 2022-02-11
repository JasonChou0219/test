import {
    Workflow, WorkflowInfoList, WorkflowInfoTuple,
    Dataflow, DataflowInfoList,
    DataProtocol, DataProtocolInfoList,
} from '@app/_models';


export enum ScheduledJobStatus {
    WAITING_FOR_EXECUTION = 0,
    SUBMITED_FOR_EXECUTION = 1,
    RUNNING = 2,
    FINISHED_SUCCESSFUL = 3,
    FINISHED_ERROR = 4,
    FINISHED_MANUALLY = 5,
    UNKNOWN = 6,
}

export interface ScheduledJob {
    id?: number;
    // uuid?: string;
    title: string;
    description?: string;
    owner: string;
    owner_id: number;

    workflows?: Workflow[];
    dataflows?: Dataflow[];
    data_protocols?: DataProtocol[];
    database: string;

    execute_at: Date;
    created_at: Date;
    scheduled_at: Date;
    job_status: typeof ScheduledJobStatus;
}

export interface ScheduledJobInfo {
    id?: number;
    // uuid?: string;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;

    workflows?: WorkflowInfoTuple[];  // WorkflowInfoList[];
    dataflows?: DataflowInfoList;
    data_protocols?: DataProtocolInfoList;
    database?: string;

    execute_at: Date;
    created_at: Date;
    scheduled_at: Date;
    job_status: typeof  ScheduledJobStatus;
}

export interface ScheduledJobInfoList {
    data: ScheduledJobInfo[];
}
