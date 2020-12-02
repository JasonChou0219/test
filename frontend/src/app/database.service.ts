import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {element} from 'protractor';
import {Device, SERVER_URL} from './device.service';
import {map} from 'rxjs/operators';

const TestDatabaseList: DatabaseList = {data: [
        {id: 1234567, name: 'deviceManagerDB', address: '127.0.0.1', port: 8888, online: true, status: 'connected'},
        {id: 44444, name: 'TestDB', address: '10.152.248.1', port: 8888, online: true, status: 'connected'},
        {id: 77666, name: 'schedulerDB', address: 'localhost', port: 8060, online: false, status: 'disconnected'}]
};

// For test purposes:
export const TestDatabase: Database = {name: 'schedulerDB', address: 'localhost', port: 8888, online: true, status: 'connected' };

export interface Database {
    // device_uuid: string;
    id?: number;
    name: string;
    address: string;
    port: number;
    online: boolean;
    status: string;
}
export interface DatabaseDeviceLink {
    deviceId: string;
    databaseId: number;
}
interface DatabaseList {
    data: Database[];
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
    async getDatabases() {
        console.log('Returning databases');
        console.log(this.databases);
        return this.databases;
    }
    // getDatabaseList will replace getDatabases once implemented in the backend
    async getDatabaseList(): Promise<Database[]> {
        return this.http
            .get<DatabaseList>(this.serverUrl + '/api/databases/')
            .pipe(map((databaseList) => databaseList.data))
            .toPromise();
        // Todo: Implement call to backend!
    }
    async getDatabase(id: string): Promise<Database> {
        // Not implemented in the backend yet
        // Not used yet
        return this.http
            .get<Database>(this.serverUrl + 'api/databases/' + id)
            .toPromise();
    }
    async setDatabase(uuid: string, database: Database) {
        // Not implemented in the backend yet
        // may not be needed. Replac by linkDatabase?
        return this.http
            .put(this.serverUrl + '/api/database/' + uuid, database)
            .toPromise();
    }
    async addDatabase(database: Database) {
        // Not implemented in backend yet
        // Will replace addDatabase
        return this.http
            .post(this.serverUrl + '/api/databases', database)
            .toPromise();
    }
    async oldAddDatabase(database: Database) {
        this.databases.push(database);
        console.log(this.databases);
    }
    async deleteDatabase(database: Database) {
        database = this.databases.find(element => element.name === database.name);
        for ( var i = 0; i < this.databases.length; i++) { if (this.databases[i] === database) {
            this.databases.splice(i, 1 ); i--; } }
        console.log('Deleting database');
        console.log(database);
        // delete this.databases[database];
        // return this.http
        //    .delete(this.serverUrl + '/api/databases/' + name)
        //    .toPromise();
    }
    async newDeleteDatabase(id: string) {
        // Will replace deleteDatabase
        // Not implemented in the backend yet
        return this.http
            .delete(this.serverUrl + '/api/databases/' + id)
            .toPromise();
    }
    async linkDatabaseToDevice(uuid: string, id: number) {
        // maybe use device, database instead of id, uuid
        // Link a database (id) to a device (uuid)
        console.log('Link data');
        console.log(uuid, id);
        return this.http
            .post(this.serverUrl + '/api/devices/' + uuid, id)
            .toPromise();
    }
    /*
    async linkDatabaseToDevice(database: Database, device: Device) {
        return this.http
            .put(this.serverUrl + '/api/device/' + device, database)
            .toPromise();
        // Todo: Add functional implementation. Create backend counterpart
        //  Fix url
    }
    '
     */
    async deleteDatabaseLinkToDevice(uuid: Device) {
        return this.http
            .delete(this.serverUrl + '/api/device/' + uuid)
            .toPromise();
        // Todo: Add functional implementation. Create backend counterpart
        //  Fix url
    }
    clearDatabases() {
        this.databases = [];
        return this.databases;
    }
    //
    // Checkmarks and polling intervals
    //
    async setPollingInterval() {
        //
    }

}
