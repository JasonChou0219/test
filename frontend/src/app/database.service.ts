import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {element} from 'protractor';
import {Device, SERVER_URL} from './device.service';
import {map} from 'rxjs/operators';

const TestDatabaseList: DatabaseList = {data: [
        {name: 'deviceManagerDB', address: '127.0.0.1', port: 8888, online: true, status: 'connected'},
        {name: 'TestDB', address: '10.152.248.1', port: 8888, online: true, status: 'connected'},
        {name: 'schedulerDB', address: 'localhost', port: 8060, online: false, status: 'disconnected'}]
};

// For test purposes:
export const TestDatabase: Database = {name: 'schedulerDB', address: 'localhost', port: 8888, online: true, status: 'connected' };

export interface Database {
    // device_uuid: string;
    name: string;
    address: string;
    port: number;
    online: boolean;
    status: string;
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
    addDatabase(database) {
        this.databases.push(database);
        console.log(this.databases);
    }
    async setDatabase(uuid: string, database: Database) {
        return this.http
            .put(this.serverUrl + '/api/database/' + uuid, database)
            .toPromise();
    }
    getDatabases() {
        console.log('Returning databases');
        console.log(this.databases);
        return this.databases;

    }
    clearDatabases() {
        this.databases = [];
        return this.databases;
    }
    deleteDatabase(database) {

        // delete this.databases[database];
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

    async getDatabaseList(): Promise<Database[]> {
        return this.http
            .get<DatabaseList>(this.serverUrl + '/api/databases/')
            .pipe(map((databaseList) => databaseList.data))
            .toPromise();
        // Todo: Implement call to backend!
    }
    async deleteDatabaseFromList(name: string) {
        return this.http
            .delete(this.serverUrl + '/api/databases/' + name)
            .toPromise();
        // Todo: Add functional implementation. Create backend counterpart!
    }
    async addDatabaseToList(database: Database) {
        return this.http
            .put(this.serverUrl + '/api/databases/' + database.name, database)
            .toPromise();
        // Todo: Add implementation call to backend!
    }
    async linkDatabaseToDevice(database: Database, device: Device) {
        return this.http
            .put(this.serverUrl + '/api/device/' + device, database)
            .toPromise();
        // Todo: Add functional implementation. Create backend counterpart
        //  Fix url
    }
    async deleteDatabaseLinkToDevice(device: Device) {
        return this.http
            .delete(this.serverUrl + '/api/device/' + device)
            .toPromise();
        // Todo: Add functional implementation. Create backend counterpart
        //  Fix url
    }
}
