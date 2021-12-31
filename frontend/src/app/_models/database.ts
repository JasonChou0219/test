export interface Database {
    id?: number;
    uuid?: string;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;
}

export interface DatabaseInfo {
    id?: number;
    uuid?: string;
    title: string;
    description?: string;
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
