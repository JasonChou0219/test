// import { ServiceInfo } from '@app/_models';
// import { Workflow, WorkflowInfo, WorkflowInfoList } from '@app/_models';
// import { Job, JobInfo } from '@app/_models'


export const mockServiceInfo = {
    uuid: '1111-2222-3333-4444-5555-6666',
    server_uuid: '2222-3333-4444-5555-6666-7777',
    name: 'Mock Service 1',
    type: 'Mock service type',
    address: '127.0.0.1',
    port: 50051,
    available: true,
    user: 0,
    databaseId: 0,
    dataHandlerActive: false,
}

export const mockServiceInfoList = [
    mockServiceInfo,
    {
        uuid: '2111-2222-3333-4444-5555-6666',
        server_uuid: '2222-3333-4444-5555-6666-7777',
        name: 'Mock Service 2',
        type: 'Mock service type',
        address: '127.0.0.1',
        port: 50052,
        available: true,
        user: 0,
        databaseId: 0,
        dataHandlerActive: false,
    },
    {
        uuid: '3111-2222-3333-4444-5555-6666',
        server_uuid: '2222-3333-4444-5555-6666-7777',
        name: 'Mock Service 3',
        type: 'Mock service type',
        address: '127.0.0.1',
        port: 50053,
        available: true,
        user: 0,
        databaseId: 0,
        dataHandlerActive: false,
    }
]

export const mockWorkflowInfo = {
    id: 1,
    title: 'Mock Workflow 1',
    fileName: '',
    workflow_type: 'python',
    services: mockServiceInfoList,
    data: 'workflow data here ...',
    owner: 'Workflow Owner',
    owner_id: 1,
    description: 'This is a workflow description',
}

export const mockWorkflowInfoList = [
    mockWorkflowInfo,
    {
        id: 2,
        title: 'Mock Workflow 2',
        fileName: '',
        workflow_type: 'python',
        services: mockServiceInfoList,
        data: 'workflow data here ...',
        owner: 'Workflow Owner',
        owner_id: 1,
        description: 'This is a workflow description',
    },
    {
        id: 3,
        title: 'Mock Workflow 3',
        fileName: '',
        workflow_type: 'node-red',
        services: mockServiceInfoList,
        data: 'workflow data here ...',
        owner: 'Workflow Owner',
        owner_id: 1,
        description: 'This is a workflow description',
    }
];


export const mockDataflowInfo = {
            id: 1,
            title: 'Mock Dataflow 1',
        }

export const mockDataflowInfoList = [{
            id: 1,
            title: 'Mock Dataflow 1',
        },
        {
            id: 2,
            title: 'Mock Dataflow 2'
        },
        {
            id: 3,
            title: 'Mock Dataflow 3'
        }
        ];


export const mockDatabaseInfo = {
            id: 1,
            title: 'Mock Database 1',
        }

export const mockDatabaseInfoList = [{
            id: 1,
            title: 'Mock Database 1',
        },
        {
            id: 2,
            title: 'Mock Database 2'
        },
        {
            id: 3,
            title: 'Mock Database 3'
        }
        ];

export const mockDataProtocolInfo = {
    id: 1,
    title: 'Mock Data Protocol 1',
    description: 'The description of mock data protocol 1.',
    owner: 'John Doe',
    owner_id: 1,
    created_at: Date(),
    execute_at: Date(),
    service: mockServiceInfo,
    database: mockDatabaseInfo,
}

export const mockDataProtocolInfoList = [
    mockDataProtocolInfo,
    {
        id: 2,
        title: 'Mock Data Protocol 2',
        description: 'The description of mock data protocol 2.',
        owner: 'John Doe',
        owner_id: 1,
        created_at: Date(),
        execute_at: Date(),
        service: mockServiceInfo,
        database: mockDatabaseInfo,
    },
    {
        id: 3,
        title: 'Mock Data Protocol 3',
        description: 'The description of mock data protocol 3.',
        owner: 'John Doe',
        owner_id: 1,
        created_at: Date(),
        execute_at: Date(),
        service: mockServiceInfo,
        database: mockDatabaseInfo,
    }
]

export const mockJobInfo = {
    id: 1,
    title: 'Mock Job 1',
    description: 'This is mock job 1 description.',
    owner: 'John Doe',
    owner_id: 1,
    execute_at: Date(),
    created_at: Date(),
    running: false,
    workflows: mockWorkflowInfoList,
    dataflows: mockDataflowInfoList,
    data_protocols: mockDataProtocolInfoList,
}

export const mockJobInfoList = [
    mockJobInfo,
    {
        id: 2,
        title: 'Mock Job 2',
        description: 'This is mock job 2 description.',
        owner: 'John Doe',
        owner_id: 1,
        execute_at: Date(),
        created_at: Date(),
        running: false,
        workflow_id: 1,
        workflow_name: 'Mock Workflow Name',
        workflow_type: 'python',
        workflow_execute_at: Date(),
        workflow_running: false,
        database_name: 'Mock Database 2',
    },
    {
        id: 3,
        title: 'Mock Job 3',
        description: 'This is mock job 3 description.',
        owner: 'John Doe',
        owner_id: 1,
        execute_at: Date(),
        created_at: Date(),
        running: false,
        workflow_id: 1,
        workflow_name: 'Mock Workflow Name',
        workflow_type: 'python',
        workflow_execute_at: Date(),
        workflow_running: false,
        database_name: 'Mock Database 3',
    }
];

export const mockBookingInfo = {
    id: 1,
    title: 'Mock Booking 1',
    description: 'Description of mock booking 1.',
    owner: 'John Doe',
    owner_id: 1,
    execute_at: Date(),
    created_at: Date(),
    running: false,
    job: mockJobInfo,
}

export const mockBookingInfoList = [
    {
        mockBookingInfo
    },
    {
        id: 2,
        title: 'Mock Booking 2',
        description: 'Description of mock booking 2.',
        owner: 'John Doe',
        owner_id: 1,
        execute_at: Date(),
        created_at: Date(),
        running: false,
        job: mockJobInfo,
    },
    {
        id: 3,
        title: 'Mock Booking 3',
        description: 'Description of mock booking 3.',
        owner: 'John Doe',
        owner_id: 1,
        execute_at: Date(),
        created_at: Date(),
        running: false,
        job: mockJobInfo,
    }
];
