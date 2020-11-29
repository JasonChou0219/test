import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { SERVER_ADDRESS, SERVER_PORT } from './device.service';

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

const WEBSOCKET_URL = `ws://${SERVER_ADDRESS}:${SERVER_PORT}/ws/experiments`;

@Injectable({
    providedIn: 'root',
})
export class ExperimentService {
    socket$; //: WebSocketSubject<ExperimentStatusMessage>;
    constructor() {
        this.socket$ = webSocket(WEBSOCKET_URL);
    }

    getExperimentStatusStream(): Observable<ExperimentStatusMessage> {
        return this.socket$.asObservable();
    }
    connect() {
        this.socket$.subscribe(
            (msg) => {
                console.log(msg);
            },
            (error) => console.log(error)
        );
    }
}
