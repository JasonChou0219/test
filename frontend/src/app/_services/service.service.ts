import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { env } from '@environments/environment';

import {SilaServerInfo, DiscoveredSilaServiceList, Service, ServiceStatus, ServiceList, ServiceUuidList,
ServiceStatusList, ServiceFeatureList, ServiceParameter, ServiceProperty, ServiceCommand, ServiceFeature} from '@app/_models';


const test_service_1: Service = {
    uuid: '0123-2445-22222221-34535235-223423',
    server_uuid: '1111-22222-3333-4444-5555-666',
    name: 'Test Service',
    type: 'Test Type',
    address: '127.0.0.1',
    port: 50051,
    available: true,
    user: 1,
    databaseId: 1,
    dataHandlerActive: false,
    }


const test_service_1_status: ServiceStatus = {
    online: true,
    status: 'Available',
}

export enum LogLevel {
    INFO = 0,
    WARNING = 1,
    CRITICAL = 2,
    ERROR = 3,
}

export interface LogEntry {
    type: LogLevel;
    service: string;
    time: number;
    message: string;
}

export interface LogFilter {
    excludeInfo: boolean;
    excludeWarn: boolean;
    excludeCritical: boolean;
    excludeError: boolean;
}

interface LogEntryList {
    data: LogEntry[];
}

export interface BookingInfo {
    id?: number;
    name: string;
    start: number;
    end: number;
    user: number;
    userName: string;
    service: string;
    serviceName: string;
    job?: number;
    jobName?: string;
}
interface BookingInfoList {
    data: BookingInfo[];
}

export interface JobBookingInfo {
    name: string;
    start: number;
    end: number;
    services: string[];
    workflowID: number;
}

export interface Job {
    id?: number;
    name: string;
    start: number;
    end: number;
    user: string;
    serviceBookings: BookingInfo[];
    workflowID: number;
    workflowName: string;
}

export interface JobStatus {
    online: boolean;
    status: string;
}


export interface JobList {
    data: Job[];
}


@Injectable({
    providedIn: 'root',
})
export class ServiceService {
    // serverUrl = env.backendHttpUrl;
    serverUrl = env.apiUrl;
    constructor(private http: HttpClient) {
    }
    async getServiceList(): Promise<Service[]> {
        // Mock implementation
        return [test_service_1]
        // Real implementation
        // return this.http
        //     .get<ServiceList>(this.serverUrl + '/api/services')
        //     .pipe(map((serviceList) => serviceList.data))
        //     .toPromise();
    }
    async getService(uuid: string): Promise<Service> {
        return this.http
            .get<Service>(this.serverUrl + '/api/services/' + uuid)
            .toPromise();
    }
    async setService(uuid: string, service: Service) {
        return this.http
            .put(this.serverUrl + '/api/services/' + uuid, service)
            .toPromise();
    }
    async addService(service: Service) {
        return this.http
            .post(this.serverUrl + '/api/services', service)
            .toPromise();
    }
    async deleteService(uuid: string) {
        return this.http
            .delete(this.serverUrl + '/api/services/' + uuid)
            .toPromise();
    }
    async getServiceStatus(uuid: string): Promise<ServiceStatus> {
    //    // Mock implementation
        return test_service_1_status
        // Real implementation
        // return this.http
        //     .get<ServiceStatus>(this.serverUrl + '/api/ServiceStatus/' + uuid)
        //     .toPromise();
    }
    getServiceFeatures(uuid: string): Promise<ServiceFeature[]> {
        return this.http
            .get<ServiceFeatureList>(
                this.serverUrl + '/api/serviceFeatures/' + uuid
            )
            .pipe(map((featureList) => featureList.data))
            .toPromise();
    }
    getServiceFeaturesDataHandler(uuid: string): Promise<ServiceFeature[]> {
        return this.http
            .get<ServiceFeatureList>(
                this.serverUrl + '/api/serviceFeaturesDataHandler/' + uuid
            )
            .pipe(map((featureList) => featureList.data))
            .toPromise();
    }
    async discoverSilaServices(): Promise<SilaServerInfo[]> {
        return this.http
            .get<DiscoveredSilaServiceList>(
                this.serverUrl + '/api/silaDiscovery/'
            )
            .pipe(map((serviceList) => serviceList.data))
            .toPromise();
    }
    async getServiceLog(param?: {
        from?: Date;
        to?: Date;
        excludeInfo?: boolean;
        excludeWarning?: boolean;
        excludeCritical?: boolean;
        excludeError?: boolean;
    }): Promise<LogEntry[]> {
        let filterString = '';
        if (param) {
            filterString += '?';
            if (param.from) {
                filterString += `start=${Math.floor(
                    param.from.getTime() / 1000
                )}`;
            }
            if (param.to) {
                const seperator = param.from ? '&' : '';
                filterString +=
                    seperator + `end=${Math.floor(param.to.getTime() / 1000)}`;
            }
            if (param.excludeInfo) {
                const seperator = param.from || param.to ? '&' : '';
                filterString += seperator + `excludeInfo=${param.excludeInfo}`;
            }
            if (param.excludeWarning) {
                const seperator =
                    param.from || param.to || param.excludeInfo ? '&' : '';
                filterString +=
                    seperator + `excludeWarning=${param.excludeWarning}`;
            }
            if (param.excludeCritical) {
                const seperator =
                    param.from ||
                    param.to ||
                    param.excludeInfo ||
                    param.excludeWarning
                        ? '&'
                        : '';
                filterString +=
                    seperator + `excludeCritical=${param.excludeCritical}`;
            }
            if (param.excludeError) {
                const seperator =
                    param.from ||
                    param.to ||
                    param.excludeInfo ||
                    param.excludeWarning ||
                    param.excludeCritical
                        ? '&'
                        : '';
                filterString +=
                    seperator + `excludeError=${param.excludeError}`;
            }
        }
        return this.http
            .get<LogEntryList>(
                this.serverUrl + '/api/serviceLog/' + filterString
            )
            .pipe(map((logEntries) => logEntries.data))
            .toPromise();
    }
}
