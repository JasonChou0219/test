export interface Workflow {
    id?: number;
    name: string;
    fileName: string;
    data: string;
}
export interface WorkflowInfo {
    id: number;
    name: string;
    fileName: string;
}

export interface WorkflowInfoList {
    data: WorkflowInfo[];
}
