import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { environment } from '../environments/environment';

export enum ExperimentStatus {
    WAITING_FOR_EXECUTION = 0,
    SUBMITED_FOR_EXECUTION = 1,
    RUNNING = 2,
    FINISHED_SUCCESSFUL = 3,
    FINISHED_ERROR = 4,
    FINISHED_MANUALLY = 5,
    UNKNOWN = 6,
}

export interface ExperimentStatusMessage {
    experimentId: number;
    status: ExperimentStatus;
}

const WEBSOCKET_URL_STATUS = `${environment.backendWebsocketsUrl}/ws/experiments_status`;

export interface ExperimentLogs {
    experimentId: number;
    logList: string[];
}
const WEBSOCKET_URL_LOGS = `${environment.backendWebsocketsUrl}/ws/experiments_logs`;

@Injectable({
    providedIn: 'root',
})
export class ExperimentService {
    statusSocket$: WebSocketSubject<ExperimentStatusMessage>;
    logsSocket$: WebSocketSubject<ExperimentLogs>;
    constructor() {
        this.statusSocket$ = webSocket(WEBSOCKET_URL_STATUS);
        this.logsSocket$ = webSocket(WEBSOCKET_URL_LOGS);
    }

    getExperimentStatusStream(): Observable<ExperimentStatusMessage> {
        return this.statusSocket$.asObservable();
    }
    getExperimentsLogsStream(): Observable<ExperimentLogs> {
        return this.logsSocket$.asObservable();
    }
}
