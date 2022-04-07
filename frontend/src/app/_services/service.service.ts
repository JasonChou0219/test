import {Injectable} from '@angular/core';
import {map} from 'rxjs/operators';
import {HttpClient, HttpParams} from '@angular/common/http';
import {env} from '@environments/environment';

import {
    DiscoveredSilaServiceList,
    Service,
    ServiceFeature,
    ServiceFeatureList,
    ServiceStatus, SilaCommand, SilaDefinedExecutionError, SilaFeatureInfo, SilaProperty,
    SilaServerInfo,
    SilaServiceInfo
} from '@app/_models';

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
    constructor(private http: HttpClient) {
    }
    // serverUrl = env.backendHttpUrl;
    serverUrl = env.apiUrl;

    async parseFeatureDefiniton(result: [SilaFeatureInfo]) {
        const parsedFeatureInfos: SilaFeatureInfo[] = [];
        for (const feature of result) {
            if (feature.commands) {
                const parsedCommands: SilaCommand[] = [];

                for (const command of Object.keys(feature.commands)) {
                    parsedCommands.push(feature.commands[command] as SilaCommand);
                }
                feature.commands = parsedCommands;
            }

            if (feature.properties) {
                const parsedProperties: SilaProperty[] = [];

                for (const property of Object.keys(feature.properties)) {
                    parsedProperties.push(feature.properties[property] as SilaProperty);
                }
                feature.properties = parsedProperties;
            }

            if (feature.errors) {
                const parsedErrors: SilaDefinedExecutionError[] = [];

                for (const command of Object.keys(feature.commands)) {
                    parsedErrors.push(feature.commands[command] as SilaDefinedExecutionError);
                }

                feature.errors = parsedErrors;
            }
            parsedFeatureInfos.push(feature);

        }
        return parsedFeatureInfos;
    }
    async getServiceList(): Promise<SilaServiceInfo[]> {
        return await this.browseServiceInfo()
    }

    async connectService(ip: string, port: number, encrypted?: boolean, reset?: boolean){

        let queryParams = new HttpParams();
        queryParams = queryParams.append('client_ip', ip)
        queryParams = queryParams.append('client_port', port)
        if (reset) {  queryParams = queryParams.append('reset', reset) }
        if (encrypted)  { queryParams = queryParams.append('encrypted', encrypted) }
        return this.http
            .get(`${env.apiUrl}/api/v1/functions/connect`, {params: queryParams})
            .toPromise()
    }

    async updateServiceInfo(uuid: string, body){
        return this.http
            .put(`${env.apiUrl}/api/v1/functions/` +  uuid,  body)
            .toPromise()
    }

    async browseServiceInfo(){
        return this.http
            .get<[SilaServiceInfo]>(`${env.apiUrl}/api/v1/functions/browse`)
            .toPromise()
    }

    async discoverServiceMDNS(){
        return this.http
            .get<[SilaServiceInfo]>(`${env.apiUrl}/api/v1/functions/discover`)
            .toPromise()
    }

    async deleteServiceInfo(uuid: string) {
        return this.http
            .delete(`${env.apiUrl}/api/v1/functions/` + uuid)
            .toPromise();
    }

    async disconnectService(uuid: string) {
        let queryParams = new HttpParams();
        queryParams = queryParams.append('service_uuid', uuid)
        return this.http
            .get(`${env.apiUrl}/api/v1/functions/disconnect`, {params: queryParams})
            .toPromise()
    }

    async browseFeatureDefinitions(uuid: string) {
        let queryParams = new HttpParams();
        queryParams = queryParams.append('service_uuid', uuid)
        return this.http
            .get<[SilaFeatureInfo]>(`${env.apiUrl}/api/v1/functions/browse_features`, {params: queryParams})
            .toPromise()
    }

    async browseParsedFeatureDefiniton(uuid: string) {
        const result = await this.browseFeatureDefinitions(uuid)
        return this.parseFeatureDefiniton(result);
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
