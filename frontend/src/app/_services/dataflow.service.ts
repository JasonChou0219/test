import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { env } from '@environments/environment';

@Injectable({
    providedIn: 'root',
})
export class DataflowService {
    serverUrl = env.apiUrl;

    constructor(private http: HttpClient) {
    }

    async getDataflowList(): Promise<any[]> {
        return this.http
            .get<any[]>(this.serverUrl + '/api/v1/dataflows/')
            .pipe()
            .toPromise();
    }
}
