import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {element} from 'protractor';
import {Device, DeviceCommand, DeviceProperty, FeatureCommandParam, SERVER_URL} from './device.service';
import {map} from 'rxjs/operators';

const TestDatabaseList: DatabaseList = {data: [
        {id: 1234567, name: 'deviceManagerDB', address: '127.0.0.1', port: 8888},
        {id: 44444, name: 'TestDB', address: '10.152.248.1', port: 8888},
        {id: 77666, name: 'schedulerDB', address: 'localhost', port: 8060}]
};

// For test purposes:
export const TestDatabase: Database = {id: 1111, name: 'schedulerDB', address: 'localhost', port: 8888};

export interface Database {
    id?: number;
    name: string;
    address: string;
    port: number;
}
export interface DatabaseDeviceLink {
    deviceId: string;
    databaseId: number;
}
interface DatabaseList {
    data: Database[];
}
export interface DatabaseStatus {
    online: boolean;
    status: string;
}
export interface CheckboxParam {
    name: string;
    value_active: boolean;
    value_meta: boolean;
}


@Injectable({
  providedIn: 'root'
})

export class DatabaseService {
    // databases = [{name: 'testDB', ip: '127.0.0.1', port: 8889, online: true, status: 'connected' },
    //             {name: 'schedulerDB', ip: 'localhost', port: 8888, online: true, status: 'connected' }];
    databases = TestDatabaseList.data;
    serverUrl = SERVER_URL;
    constructor(private http: HttpClient) {
    }
    async getDatabases(): Promise<Database[]> {
        console.log('GetDatabases is executing......');
        return this.http
            .get<DatabaseList>(this.serverUrl + '/api/databases/')
            .pipe(map((databaseList) => databaseList.data))
            .toPromise();
    }
    async getDatabase(id: number): Promise<Database> {
        return this.http
            .get<Database>(this.serverUrl + '/api/databases/' + id)
            .toPromise();
    }
    async getDatabaseStatus(id: number): Promise<DatabaseStatus> {
        return this.http
            .get<DatabaseStatus>(this.serverUrl + '/api/databaseStatus/' + id)
            .toPromise();
    }
    async setDatabase(uuid: string, database: Database) {
        return this.http
            .put(this.serverUrl + '/api/database/' + uuid, database)
            .toPromise();
    }
    async addDatabase(database: Database) {
        return this.http
            .post(this.serverUrl + '/api/databases', database)
            .toPromise();
    }
    async deleteDatabase(id: string) {
        return this.http
            .delete(this.serverUrl + '/api/databases/' + id)
            .toPromise();
    }
    async linkDatabaseToDevice(uuid: string, id: number) {
        return this.http
            .put(this.serverUrl + '/api/devices/' + uuid + '/database', id)
            .toPromise();
    }
    async deleteDatabaseLinkToDevice(uuid: string) {
        return this.http
            .delete(this.serverUrl + '/api/devices/' + uuid + '/database')
            .toPromise();
    }
    clearDatabases() {
        this.databases = [];
        return this.databases;
    }

    async setCheckboxDeviceLevel(uuid: string, active: boolean) {
        return this.http
            .put(this.serverUrl + '/api/devices/' + uuid + '/dataHandler', active)
            .toPromise();
    }
    async setCheckboxFeatureLevel(uuid: string, featureId: number, active: boolean, meta: boolean) {
        return this.http
            .put(this.serverUrl + '/api/devices/' + uuid + '/features/' + featureId + '/dataHandler', {active, meta})
            .toPromise();
    }
    async setCheckboxCommandLevel(uuid: string, featureId: number, commandId: number, meta: boolean, active: boolean,
                                  metaInterval: number, nonMetaInterval: number, parameters: FeatureCommandParam[]) {
        return this.http
            .put(this.serverUrl + '/api/devices/' + uuid + '/features/' + featureId + '/commands/' + commandId +
                '/dataHandler', {parameters, active, meta, nonMetaInterval, metaInterval})
            .toPromise();
    }
    async setCheckboxPropertyLevel(uuid: string, featureId: number, propertyId: number, meta: boolean, active: boolean,
                                   metaInterval: number, nonMetaInterval: number) {
    }

}
