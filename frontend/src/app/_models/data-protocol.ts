// import {Database} from "./database";
import { Service, ServiceInfo, Database, DatabaseInfo } from '@app/_models'

export interface DataProtocol {
    id?: number;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;
    created_at?: Date;
    execute_at?: Date;
    service?: Service;
    database?: Database;
}

export interface DataProtocolInfo {
    id?: number;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;
    created_at?: Date;
    execute_at?: Date;
    service?: ServiceInfo;
    database?: DatabaseInfo;
}

export interface DataProtocolInfoList {
    data: DataProtocolInfo[];
}

export interface DataProtocolStatus {
    online: boolean;
    status: string;
}
