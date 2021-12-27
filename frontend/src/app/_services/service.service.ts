import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { env } from '@environments/environment';

import {SilaServerInfo, DiscoveredSilaServiceList, Service, ServiceStatus, ServiceList, ServiceUuidList,
ServiceStatusList, ServiceFeatureList, ServiceParameter, ServiceProperty, ServiceCommand, ServiceFeature} from '@app/_models';


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
        // Mock implementation
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
    async callFeatureCommand(
        service: string,
        featureOriginator: string,
        featureCategory: string,
        featureIdentifier: string,
        featureVersionMajor: number,
        command: string,
        params: FeatureCommandParam[]
    ): Promise<FeatureCommandResult[]> {
        return this.http
            .post<FeatureCommandResult[]>(
                this.serverUrl +
                    `/api/service/${service}/qualifiedFeatureIdentifier/${featureOriginator}/${featureCategory}/${featureIdentifier}/v${String(featureVersionMajor)}/command/${command}`,
                { params }
            )
            .toPromise();
    }
    async getFeatureProperty(
        service: string,
        featureOriginator: string,
        featureCategory: string,
        featureIdentifier: string,
        featureVersionMajor: number,
        property: string
    ): Promise<FeaturePropertyResult[]> {
        return this.http
            .get<FeaturePropertyResult[]>(
                this.serverUrl +
                    `/api/service/${service}/qualifiedFeatureIdentifier/${featureOriginator}/${featureCategory}/${featureIdentifier}/v${String(featureVersionMajor)}/property/${property}`
            )
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
    async getBookingInfo(from?: Date, to?: Date): Promise<BookingInfo[]> {
        let filterString = '';
        if (from && to) {
            filterString += `?start=${Math.floor(from.getTime() / 1000)}&end=${
                to.getTime() / 1000
            }`;
        } else if (!from) {
            if (to) {
                filterString += `?end=${Math.floor(to.getTime() / 1000)}`;
            }
        } else if (!to) {
            if (from) {
                filterString += `?start=${Math.floor(from.getTime() / 1000)}`;
            }
        }
        return this.http
            .get<BookingInfoList>(
                this.serverUrl + `/api/bookings${filterString}`
            )
            .pipe(map((bookingInfoList) => bookingInfoList.data))
            .toPromise();
    }
    async bookService(
        bookingName: string,
        startTime: number,
        stopTime: number,
        userID: number,
        serviceUUID: string
    ) {
        return this.http
            .post(this.serverUrl + '/api/bookings', {
                name: bookingName,
                start: startTime,
                end: stopTime,
                user: userID,
                service: serviceUUID,
            })
            .toPromise();
    }
    async deleteBooking(id: number) {
        return this.http
            .delete(this.serverUrl + '/api/bookings/' + id)
            .toPromise();
    }
    async createJob(job: JobBookingInfo) {
        return this.http
            .post(this.serverUrl + '/api/jobs', job)
            .toPromise();
    }
    async editJob(
        jobID: number,
        job: JobBookingInfo
    ) {
        return this.http
            .put(
                this.serverUrl + '/api/jobs/edit/' + jobID,
                job
            )
            .toPromise();
    }
    async getJobs(): Promise<Job[]> {
        return this.http
            .get<JobList>(this.serverUrl + '/api/jobs')
            .pipe(map((jobs) => jobs.data))
            .toPromise();
    }
    async deleteJob(id: number) {
        return this.http
            .delete(this.serverUrl + '/api/jobs/' + id)
            .toPromise();
    }
}
