// import {Database} from "./database";
import { Service, ServiceInfo, Database, DatabaseInfo } from '@app/_models'

export interface Protocol {
    id?: number;
    title: string;
    service: ProtocolService;
    custom_data?: {[key: string]: string};
    owner?: string;
    owner_id?: number;
}

export interface ProtocolInfo {
    id?: number;
    title: string;
    service: ProtocolServiceInfo;
    custom_data?: {[key: string]: string};
    owner?: string;
    owner_id?: number;
}

export interface ProtocolService {
    uuid: string;
    features: ProtocolFeature[];
}

export interface ProtocolServiceInfo {
    uuid: string;
    features: ProtocolFeatureInfo[];
}

export interface ProtocolFeature {
    identifier: string;
    commands: ProtocolCommand[];
    properties: ProtocolProperty[];
}

export interface ProtocolFeatureInfo {
    identifier: string;
    commands: ProtocolCommandInfo[];
    properties: ProtocolPropertyInfo[];
}

export interface ProtocolCommand {
    identifier: string;
    observable: boolean;
    meta: boolean;
    interval: number;
    parameters: ProtocolParameter[];
    responses: ProtocolResponse[];
}

export interface ProtocolCommandInfo {
    identifier: string;
    observable: boolean;
    meta: boolean;
    interval: number;
    parameters: ProtocolParameterInfo[];
    responses: ProtocolResponseInfo[];
}

export interface ProtocolParameter {
    identifier: string;
    value: string;
}

export interface ProtocolParameterInfo {
    identifier: string;
    value: string;
}

export interface ProtocolResponse {
    identifier: string;
}

export interface ProtocolResponseInfo {
    identifier: string;
}

export interface ProtocolProperty {
    identifier: string;
    observable: boolean;
    meta: boolean;
    interval: number;
}

export interface ProtocolPropertyInfo {
    identifier: string;
    observable: boolean;
    meta: boolean;
    interval: number;
}

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
