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
}

export interface DataflowInfoList {
    data: DataflowInfo[];
}

export interface DataflowStatus {
    online: boolean;
    status: string;
}



export const mock_dataflow_info = {
            id: 1,
            title: 'Mock Dataflow 1',
        }

export const mock_dataflow_info_list = [{
            id: 1,
            title: 'Mock Dataflow 1',
        },
        {
            id: 2,
            title: 'Mock Dataflow 2'
        },
        {
            id:3,
            title: 'Mock Dataflow 3'
        }
        ];
