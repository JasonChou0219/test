export interface Database {
    id?: number;
    title: string;
    description?: string;
    name: string;
    username: string;
    password: string;
    address: string;
    port: number;
    retention_policy: string;
    owner?: string;
    owner_id?: number;
}

export interface DatabaseInfo {
    id?: number;
    title: string;
    description?: string;
    name: string;
    username: string;
    password: string;
    address: string;
    port: number;
    retention_policy: string;
    owner?: string;
    owner_id?: number;
}

export interface DatabaseInfoList {
    data: DatabaseInfo[];
}

export interface DatabaseStatus {
    online: boolean;
    status: string;
}
