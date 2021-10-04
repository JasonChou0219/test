import { Component, OnInit, ViewChild } from '@angular/core';
import {
    animate,
    state,
    style,
    transition,
    trigger,
} from '@angular/animations';

import {
    DeviceService,
    DeviceType,
    Device,
    DeviceStatus,
    DeviceUuidList,
} from '../device.service';

import { MatDialog } from '@angular/material/dialog';
import { MatTable } from '@angular/material/table';
import { DeviceDetailComponent } from '../device-detail/device-detail.component';
import { EditDeviceComponent } from '../edit-device/edit-device.component';
import { AddDeviceComponent } from '../add-device/add-device.component';

interface RowData {
    device: Device;
    status: DeviceStatus;
    detailsLoaded: boolean;
}

@Component({
    selector: 'app-device-list',
    templateUrl: './device-list.component.html',
    styleUrls: ['./device-list.component.scss'],
    animations: [
        trigger('detailExpand', [
            state('collapsed', style({ height: '0px', minHeight: '0' })),
            state('expanded', style({ height: '*' })),
            transition(
                'expanded <=> collapsed',
                animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')
            ),
        ]),
    ],
})
export class DeviceListComponent implements OnInit {
    dataSource: RowData[] = [];
    tableColumns = [
        'name',
        'type',
        'address',
        'port',
        'free',
        'online',
        'status',
        'edit',
    ];
    selected: number | null = null;

    @ViewChild(MatTable) table: MatTable<any>;
    constructor(
        public deviceService: DeviceService,
        public dialog: MatDialog
    ) {}

    async getDevices() {
        const deviceList = await this.deviceService.getDeviceList();
        const data: RowData[] = [];
        for (const dev of deviceList) {
            data.push({
                device: dev,
                status: { online: false, status: '' },
                detailsLoaded: false,
            });
        }
        this.dataSource = data;
        this.table.renderRows();
        for (let i = 0; i < this.dataSource.length; i++) {
            const promise = this.deviceService.getDeviceStatus(
                this.dataSource[i].device.uuid
            );
            promise.then((status) => {
                this.dataSource[i].status = status;
                this.table.renderRows();
            });
        }
    }
    /*
    async getDevices() {
        const deviceList = await this.deviceService.getDeviceList();
        const data: RowData[] = [];
        for (const dev of deviceList) {
            data.push({
                device: dev,
                status: { online: false, status: '' },
                detailsLoaded: false,
            });
        }
        this.dataSource = data;
        this.table.renderRows();
        // const deviceUuidList: DeviceUuidList = {data: []};
        const deviceUuidList: string[] = [];
        for (let i = 0; i < this.dataSource.length; i++) {
            deviceUuidList.push(
                this.dataSource[i].device.uuid
            );
        }
        const deviceStatusList = await this.deviceService.getDeviceStatusList(deviceUuidList);
        console.log('heya');
        console.log(deviceStatusList);
        for (let i = 0; i < this.dataSource.length; i++) {
            this.dataSource[i].status = deviceStatusList.data[i];
        }
        console.log('hoo')
        this.table.renderRows();

        for (let i = 0; i < this.dataSource.length; i++) {
            const promise = this.deviceService.getDeviceStatus(
                this.dataSource[i].device.uuid
            );
            await promise.then((status) => {
                this.dataSource[i].status = status;
                this.table.renderRows();
            });
        }

    }
    */
    async add() {
        const dialogRef = this.dialog.open(AddDeviceComponent, {
            width: '100%',
        });
        const result = await dialogRef.afterClosed().toPromise();
        await this.deviceService.addDevice(result);
        await this.refresh();
    }

    async edit(i: number) {
        const dialogRef = this.dialog.open(EditDeviceComponent, {
            data: this.dataSource[i].device,
        });
        const result = await dialogRef.afterClosed().toPromise();
        await this.deviceService.setDevice(result.uuid, result);
        await this.refresh();
    }

    async delete(i: number) {
        await this.deviceService.deleteDevice(this.dataSource[i].device.uuid);
        await this.refresh();
    }

    async refresh() {
        await this.getDevices();
    }

    expand(i: number) {
        this.selected = this.selected === i ? null : i;
        this.dataSource[i].detailsLoaded = true;
    }

    ngOnInit() {
        this.getDevices();
    }
}
