import {Database, DatabaseInfo} from '@app/_models'

export interface Dataflow {
    id?: number;
    uuid?: string;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;
    dataflow?: string;  // The dataflow file
    dataflow_path?: string;  // The path to the dataflow API
    created_at?: Date;
    execute_at?: Date;
    database?: Database;
}

export interface DataflowInfo {
    id?: number;
    uuid?: string;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;
    dataflow_path?: string;  // The path to the dataflow API
    created_at?: Date;
    execute_at?: Date;
    database?: DatabaseInfo;
}

export interface DataflowInfoList {
    data: DataflowInfo[];
}

export interface DataflowStatus {
    online: boolean;
    status: string;
}
