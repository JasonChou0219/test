import { ServiceInfo } from '@app/_models';
import { mock_service_info_list } from './service';

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

export const mock_workflow_info = {
    id: 1,
    name: 'Mock Workflow 1',
    fileName: '',
    services: mock_service_info_list,
    data: 'workflow data here ...',
    owner: 'Workflow Owner',
    owner_id: 1,
    description: 'This is a workflow description',
}

export const mock_workflow_info_list = [
    {
        id: 1,
        name: 'Mock Workflow 1',
        fileName: '',
        services: mock_service_info_list,
        data: 'workflow data here ...',
        owner: 'Workflow Owner',
        owner_id: 1,
        description: 'This is a workflow description',
    },
    {
        id: 2,
        name: 'Mock Workflow 2',
        fileName: '',
        services: mock_service_info_list,
        data: 'workflow data here ...',
        owner: 'Workflow Owner',
        owner_id: 1,
        description: 'This is a workflow description',
    },
    {
        id: 3,
        name: 'Mock Workflow 3',
        fileName: '',
        services: mock_service_info_list,
        data: 'workflow data here ...',
        owner: 'Workflow Owner',
        owner_id: 1,
        description: 'This is a workflow description',
    }
];
