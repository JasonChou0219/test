import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DatabaseService, Database } from './database.service';

export enum DeviceType {
    SILA = 0,
    CUSTOM,
    SOFT,
}

export interface SilaServerInfo {
    uuid: string;
    name: string;
    address: string;
    hostname: string;
    port: number;
}

interface DiscoveredSilaDeviceList {
    data: SilaServerInfo[];
}

export interface Device {
    // Todo: Add id which is set by the database for each command. This way, the command (value/interval) can be changed
    //  more rapidly/easily in the backend
    uuid?: string;
    server_uuid: string;
    name: string;
    type: DeviceType;
    address: string;
    port: number;
    available?: boolean;
    user?: number;
    databaseId?: number;
    dataHandlerActive: boolean;
}

export interface DeviceStatus {
    online: boolean;
    status: string;
}

interface DeviceList {
    data: Device[];
}

export interface DeviceUuidList {
    data: string[];
}

interface DeviceStatusList {
    data: DeviceStatus[];
}

interface DeviceFeatureList {
    data: DeviceFeature[];
}

export interface DeviceParameter {
    // Todo: Add id which is set by the database for each command. This way, the command (value/interval) can be changed
    //  more rapidly/easily in the backend
    id?: number; // May not be in the correct order yet
    type: string;
    identifier: string;
    name: string;
    description: string;
    // Todo: Which datatype is suited best for value?
    value: string; // May not be in the correct order yet
}

export interface DeviceProperty {
    // Todo: Add id which is set by the database for each command. This way, the command (value/interval) can be changed
    //  more rapidly/easily in the backend
    id?: number; // May not be in the correct order yet
    identifier: string;
    name: string;
    description: string;
    observable: boolean;
    response: DeviceParameter;
    defined_execution_errors: string[];
    polling_interval_non_meta: number; // May not be
    polling_interval_meta: number; // May not be in the correct order yet
    active: boolean; // May not be in the correct order yet
    meta: boolean; // May not be in the correct order yet
}

export interface DeviceCommand {
    // Todo: Add id which is set by the database for each command. This way, the command (value/interval) can be changed
    //  more rapidly/easily in the backend
    id?: number; // May not be in the correct order yet
    identifier: string;
    name: string;
    description: string;
    observable: boolean;
    parameters: DeviceParameter[];
    responses: DeviceParameter[];
    intermediates: DeviceParameter[];
    defined_execution_errors?: string[];
    polling_interval_non_meta: number; // May not be in the correct order yet
    polling_interval_meta: number; // May not be in the correct order yet
    active: boolean; // May not be in the correct order yet
    meta: boolean; // May not be in the correct order yet
}

export interface DeviceFeature {
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
    commands: DeviceCommand[];
    properties: DeviceProperty[];
    active: boolean;
    meta: boolean;
}

export enum LogLevel {
    INFO = 0,
    WARNING = 1,
    CRITICAL = 2,
    ERROR = 3,
}

export interface LogEntry {
    type: LogLevel;
    device: string;
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
    device: string;
    deviceName: string;
    experiment?: number;
    experimentName?: string;
}
interface BookingInfoList {
    data: BookingInfo[];
}

export interface ExperimentBookingInfo {
    name: string;
    start: number;
    end: number;
    devices: string[];
    scriptID: number;
}

export interface Experiment {
    id?: number;
    name: string;
    start: number;
    end: number;
    user: string;
    deviceBookings: BookingInfo[];
    scriptID: number;
    scriptName: string;
}

export interface ExperimentList {
    data: Experiment[];
}

export interface Script {
    id?: number;
    name: string;
    fileName: string;
    data: string;
}
export interface ScriptInfo {
    id: number;
    name: string;
    fileName: string;
}

export interface ScriptInfoList {
    data: ScriptInfo[];
}

export interface FeaturePropertyResult {
    name: string;
    value: any;
}
export interface FeatureCommandParam {
    name: string;
    value: any;
}
export interface FeatureCommandResult {
    name: string;
    value: any;
}

export const SERVER_ADDRESS = 'localhost';
// export const SERVER_ADDRESS = '10.152.248.14';
export const SERVER_PORT = '5000';
export const SERVER_URL = `http://${SERVER_ADDRESS}:${SERVER_PORT}`;

@Injectable({
    providedIn: 'root',
})
export class DeviceService {
    serverUrl = SERVER_URL;
    deviceTypeMap: Map<DeviceType, string>;
    constructor(private http: HttpClient) {
        this.deviceTypeMap = new Map<DeviceType, string>([
            [DeviceType.SILA, 'Sila'],
            [DeviceType.CUSTOM, 'Custom'],
            [DeviceType.SOFT, 'Software Sensor'],
        ]);
    }
    deviceTypeAsName(type: DeviceType): string {
        return this.deviceTypeMap.get(type);
    }
    async getDeviceList(): Promise<Device[]> {
        return this.http
            .get<DeviceList>(this.serverUrl + '/api/devices')
            .pipe(map((deviceList) => deviceList.data))
            .toPromise();
    }
    async getDevice(uuid: string): Promise<Device> {
        return this.http
            .get<Device>(this.serverUrl + '/api/devices/' + uuid)
            .toPromise();
    }
    async setDevice(uuid: string, device: Device) {
        return this.http
            .put(this.serverUrl + '/api/devices/' + uuid, device)
            .toPromise();
    }
    async addDevice(device: Device) {
        return this.http
            .post(this.serverUrl + '/api/devices', device)
            .toPromise();
    }
    async deleteDevice(uuid: string) {
        return this.http
            .delete(this.serverUrl + '/api/devices/' + uuid)
            .toPromise();
    }
    async getDeviceStatus(uuid: string): Promise<DeviceStatus> {
        return this.http
            .get<DeviceStatus>(this.serverUrl + '/api/deviceStatus/' + uuid)
            .toPromise();
    }
    getDeviceFeatures(uuid: string): Promise<DeviceFeature[]> {
        return this.http
            .get<DeviceFeatureList>(
                this.serverUrl + '/api/deviceFeatures/' + uuid
            )
            .pipe(map((featureList) => featureList.data))
            .toPromise();
    }
    getDeviceFeaturesDataHandler(uuid: string): Promise<DeviceFeature[]> {
        return this.http
            .get<DeviceFeatureList>(
                this.serverUrl + '/api/deviceFeaturesDataHandler/' + uuid
            )
            .pipe(map((featureList) => featureList.data))
            .toPromise();
    }
    async callFeatureCommand(
        device: string,
        feature: string,
        command: string,
        params: FeatureCommandParam[]
    ): Promise<FeatureCommandResult[]> {
        return this.http
            .post<FeatureCommandResult[]>(
                this.serverUrl +
                    `/api/device/${device}/feature/${feature}/command/${command}`,
                { params }
            )
            .toPromise();
    }
    async getFeatureProperty(
        device: string,
        feature: string,
        property: string
    ): Promise<FeaturePropertyResult[]> {
        return this.http
            .get<FeaturePropertyResult[]>(
                this.serverUrl +
                    `/api/device/${device}/feature/${feature}/property/${property}`
            )
            .toPromise();
    }
    async discoverSilaDevices(): Promise<SilaServerInfo[]> {
        return this.http
            .get<DiscoveredSilaDeviceList>(
                this.serverUrl + '/api/silaDiscovery/'
            )
            .pipe(map((deviceList) => deviceList.data))
            .toPromise();
    }
    async getDeviceLog(param?: {
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
                this.serverUrl + '/api/deviceLog/' + filterString
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
    async bookDevice(
        bookingName: string,
        startTime: number,
        stopTime: number,
        userID: number,
        deviceUUID: string
    ) {
        return this.http
            .post(this.serverUrl + '/api/bookings', {
                name: bookingName,
                start: startTime,
                end: stopTime,
                user: userID,
                device: deviceUUID,
            })
            .toPromise();
    }
    async deleteBooking(id: number) {
        return this.http
            .delete(this.serverUrl + '/api/bookings/' + id)
            .toPromise();
    }
    async createExperiment(experiment: ExperimentBookingInfo) {
        return this.http
            .post(this.serverUrl + '/api/experiments', experiment)
            .toPromise();
    }
    async getExperiments(): Promise<Experiment[]> {
        return this.http
            .get<ExperimentList>(this.serverUrl + '/api/experiments')
            .pipe(map((experiments) => experiments.data))
            .toPromise();
    }
    async deleteExperiment(id: number) {
        return this.http
            .delete(this.serverUrl + '/api/experiments/' + id)
            .toPromise();
    }
    async startExperiment(experimentID: number) {
        return this.http
            .put(this.serverUrl + `/api/experiments/${experimentID}/status`, {
                running: true,
            })
            .toPromise();
    }
    async stopExperiment(experimentID: number) {
        return this.http
            .put(this.serverUrl + `/api/experiments/${experimentID}/status`, {
                running: false,
            })
            .toPromise();
    }
    async getExperimentStatus(id: number): Promise<DeviceStatus> {
        return this.http
            .get<DeviceStatus>(this.serverUrl + '/api/deviceStatus/' + id)
            .toPromise();
    }
    async getUserScriptsInfo(): Promise<ScriptInfo[]> {
        return this.http
            .get<ScriptInfoList>(this.serverUrl + '/api/scripts')
            .pipe(map((script) => script.data))
            .toPromise();
    }
    async getUserScript(scriptID: number): Promise<Script> {
        return this.http
            .get<Script>(this.serverUrl + '/api/scripts/' + scriptID)
            .toPromise();
    }
    async setUserScriptInfo(scriptInfo: ScriptInfo) {
        return this.http
            .put(
                this.serverUrl + `/api/scripts/${scriptInfo.id}/info`,
                scriptInfo
            )
            .toPromise();
    }
    async setUserScript(script: Script) {
        return this.http
            .put(this.serverUrl + `/api/scripts/${script.id}/`, script)
            .toPromise();
    }
    async createUserScript(script: Script) {
        return this.http
            .post(this.serverUrl + '/api/scripts', script)
            .toPromise();
    }
    async deleteUserScript(scriptID: number) {
        return this.http
            .delete(this.serverUrl + '/api/scripts/' + scriptID)
            .toPromise();
    }
}
