import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { DeviceService, Device, DeviceType } from '../device.service';

@Component({
    selector: 'app-add-device',
    templateUrl: './add-device.component.html',
    styleUrls: ['./add-device.component.scss'],
})
export class AddDeviceComponent implements OnInit {
    deviceTypes = [
        {
            value: DeviceType.SILA,
            name: this.deviceService.deviceTypeAsName(DeviceType.SILA),
        },
        {
            value: DeviceType.CUSTOM,
            name: this.deviceService.deviceTypeAsName(DeviceType.CUSTOM),
        },
        {
            value: DeviceType.SOFT,
            name: this.deviceService.deviceTypeAsName(DeviceType.SOFT),
        },
    ];
    dataSource = [];
    tableColumns = ['uuid', 'name', 'address', 'port', 'hostname', 'select'];

    discoveryStarted = false;
    device: Device;
    constructor(
        public deviceService: DeviceService,
        public dialogRef: MatDialogRef<AddDeviceComponent>
    ) {
        this.device = {
            uuid: '',
            name: '',
            type: DeviceType.SILA,
            address: '',
            port: 80,
            available: true,
        };
    }
    select(i: number) {
        this.device.uuid = this.dataSource[i].uuid;
        this.device.name = this.dataSource[i].name;
        this.device.address = this.dataSource[i].ip;
        this.device.port = this.dataSource[i].port;
    }
    async discovery() {
        this.discoveryStarted = true;
        this.dataSource = await this.deviceService.discoverSilaDevices();
    }

    ngOnInit(): void {}
}
