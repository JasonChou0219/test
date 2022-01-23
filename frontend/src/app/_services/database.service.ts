import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { env } from '@environments/environment';

import { Database, DatabaseInfo, DatabaseInfoList, DatabaseStatus } from '@app/_models';

@Injectable({
    providedIn: 'root',
})
export class DatabaseService {
    constructor(private http: HttpClient) {
    }

    async getDatabaseList(): Promise<DatabaseInfo[]> {
        return this.http
            .get<DatabaseInfo[]>(`${env.apiUrl}:81/api/v1/databases/`) // TODO port in env
            .pipe(map((database) => database))
            .toPromise();
    }
    async getDatabase(databaseID: number): Promise<Database> {
        return this.http
            .get<Database>(`${env.apiUrl}:81/api/v1/databases/${databaseID}/`) // TODO port in env
            .toPromise();
    }
    async setDatabaseInfo(databaseInfo: DatabaseInfo) {
        return this.http
            .put(
                `${env.apiUrl}:81/api/v1/databases/${databaseInfo.id}/`, // TODO port in env
                databaseInfo
            )
            .toPromise();
    }
    async setDatabase(database: Database) {
        return this.http
            .put(`${env.apiUrl}:81/api/v1/databases/${database.id}/`, database) // TODO port in env
            .toPromise();
    }
    async createDatabase(database: DatabaseInfo) {
        return this.http
            .post(`${env.apiUrl}:81/api/v1/databases/`, database) // TODO port in env
            .toPromise();
    }
    async deleteDatabase(databaseID: number) {
        return this.http
            .delete(`${env.apiUrl}:81/api/v1/databases/${databaseID}/`) // TODO port in env
            .toPromise();
    }

    async getDatabaseStatus(databaseID: number): Promise<DatabaseStatus> {
        return this.http
            .get<DatabaseStatus>(`${env.apiUrl}:81/api/v1/databases/${databaseID}/status/`) // TODO port in env
            .toPromise();
    }
}
