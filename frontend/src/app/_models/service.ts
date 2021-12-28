export interface SilaServerInfo {
    uuid: string;
    name: string;
    address: string;
    hostname: string;
    port: number;
}

export interface DiscoveredSilaServiceList {
    data: SilaServerInfo[];
}

export interface Service {
    // Todo: Add id which is set by the database for each command. This way, the command (value/interval) can be changed
    //  more rapidly/easily in the backend
    uuid?: string;
    server_uuid: string;
    name: string;
    type: string;
    address: string;
    port: number;
    available?: boolean;
    user?: number;
    databaseId?: number;
    dataHandlerActive: boolean;
}

export interface ServiceInfo {
    // Todo: Add id which is set by the database for each command. This way, the command (value/interval) can be changed
    //  more rapidly/easily in the backend
    uuid?: string;
    server_uuid: string;
    name: string;
    type: string;
    address: string;
    port: number;
    available?: boolean;
    user?: number;
    databaseId?: number;
    dataHandlerActive: boolean;
}

export interface ServiceStatus {
    online: boolean;
    status: string;
}

export interface ServiceList {
    data: Service[];
}

export interface ServiceUuidList {
    data: string[];
}

export interface ServiceStatusList {
    data: ServiceStatus[];
}

export interface ServiceFeatureList {
    data: ServiceFeature[];
}

export interface ServiceParameter {
    // Todo: Add id which is set by the database for each command. This way, the command (value/interval) can be changed
    //  more rapidly/easily in the backend
    id?: number; // May not be in the correct order yet
    data_type: string;
    identifier: string;
    display_name: string;
    description: string;
    // Todo: Which datatype is suited best for value?
    value: string; // May not be in the correct order yet
}

export interface ServiceProperty {
    // Todo: Add id which is set by the database for each command. This way, the command (value/interval) can be changed
    //  more rapidly/easily in the backend
    id?: number; // May not be in the correct order yet
    identifier: string;
    name: string;
    description: string;
    observable: boolean;
    response: ServiceParameter;
    defined_execution_errors: string[];
    polling_interval_non_meta: number; // May not be
    polling_interval_meta: number; // May not be in the correct order yet
    active: boolean; // May not be in the correct order yet
    meta: boolean; // May not be in the correct order yet
}

export interface ServiceCommand {
    // Todo: Add id which is set by the database for each command. This way, the command (value/interval) can be changed
    //  more rapidly/easily in the backend
    id?: number; // May not be in the correct order yet
    identifier: string;
    name: string;
    description: string;
    observable: boolean;
    parameters: ServiceParameter[];
    responses: ServiceParameter[];
    intermediates: ServiceParameter[];
    defined_execution_errors?: string[];
    polling_interval_non_meta: number; // May not be in the correct order yet
    polling_interval_meta: number; // May not be in the correct order yet
    active: boolean; // May not be in the correct order yet
    meta: boolean; // May not be in the correct order yet
}

export interface ServiceFeature {
    // Todo: Add id which is set by the database for each command. This way, the command (value/interval) can be changed
    //  more rapidly/easily in the backend
    id?: number; // May not be in the correct order yet
    identifier: string;
    name: string;
    description: string;
    sila2_version?: string;
    category?: string;
    maturity_level?: string;
    locale?: string;
    originator?: string;
    feature_version: string;
    feature_version_minor: number;
    feature_version_major: number;
    commands: ServiceCommand[];
    properties: ServiceProperty[];
    active: boolean;
    meta: boolean;
}

export const mock_service_info = {
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

export const mock_service_info_list = [
    {
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
    },
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
