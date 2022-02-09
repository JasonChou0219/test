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
            .get<DatabaseInfo[]>(`${env.apiUrl}/api/v1/databases/`)
            .pipe(map((database) => database))
            .toPromise();
    }
    async getDatabase(databaseID: number): Promise<Database> {
        return this.http
            .get<Database>(`${env.apiUrl}/api/v1/databases/${databaseID}/`)
            .toPromise();
    }
    async setDatabaseInfo(databaseInfo: DatabaseInfo) {
        return this.http
            .put(
                `${env.apiUrl}/api/v1/databases/${databaseInfo.id}/`,
                databaseInfo
            )
            .toPromise();
    }
    async setDatabase(database: Database) {
        return this.http
            .put(`${env.apiUrl}/api/v1/databases/${database.id}/`, database)
            .toPromise();
    }
    async createDatabase(database: DatabaseInfo) {
        return this.http
            .post(`${env.apiUrl}/api/v1/databases/`, database)
            .toPromise();
    }
    async deleteDatabase(databaseID: number) {
        return this.http
            .delete(`${env.apiUrl}/api/v1/databases/${databaseID}/`)
            .toPromise();
    }

    async getDatabaseStatus(databaseID: number): Promise<DatabaseStatus> {
        return this.http
            .get<DatabaseStatus>(`${env.apiUrl}/api/v1/databases/${databaseID}/status/`)
            .toPromise();
    }
}
