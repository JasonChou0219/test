import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { env } from '@environments/environment';

import {Protocol, ProtocolInfo} from '@app/_models';

@Injectable({
    providedIn: 'root',
})
export class ProtocolService {
    constructor(private http: HttpClient) {
    }

    async getProtocolInfoList(): Promise<ProtocolInfo[]> {
        return this.http
            .get<ProtocolInfo[]>(`${env.apiUrl}/api/v1/protocols/`)
            .pipe(map((protocol) => protocol))
            .toPromise();
    }

    async getProtocol(protocolID: number): Promise<Protocol> {
        return this.http
            .get<Protocol>(`${env.apiUrl}/api/v1/protocols/${protocolID}/`)
            .toPromise();
    }

    async setProtocol(protocol: Protocol) {
        return this.http
            .put(`${env.apiUrl}/api/v1/protocols/${protocol.id}/`, protocol)
            .toPromise();
    }

    async setProtocolInfo(protocolInfo: ProtocolInfo) {
        return this.http
            .put(`${env.apiUrl}/api/v1/protocols/${protocolInfo.id}/`, protocolInfo)
            .toPromise();
    }
    async createProtocol(protocolInfo: ProtocolInfo) {
        return this.http
            .post(`${env.apiUrl}/api/v1/protocols/`, protocolInfo)
            .toPromise();
    }
    async deleteProtocol(protocolID: number) {
        return this.http
            .delete(`${env.apiUrl}/api/v1/protocols/${protocolID}/`)
            .toPromise();
    }
}
