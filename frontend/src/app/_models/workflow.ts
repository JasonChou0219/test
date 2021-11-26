export interface Workflow {
    id?: number;
    name: string;
    fileName: string;
    services?: string[];
    data: string;
    owner?: string;
    owner_id?: number;
    description?: string;
}
export interface WorkflowInfo {
    id?: number;
    name: string;
    fileName: string;
    services?: string[];
    data: string;
    owner?: string;
    owner_id?: number;
    description?: string;
    //
    //id: number;
    //name: string;
    //fileName: string;
    //owner?: string;
    //owner_id?: number;
}

export interface WorkflowInfoList {
    // data: WorkflowInfo[];
    data: WorkflowInfo[];
}
