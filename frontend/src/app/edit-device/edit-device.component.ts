import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Device, DeviceService, DeviceType } from '../device.service';
import { identifierModuleUrl } from '@angular/compiler';

@Component({
    selector: 'app-edit-device',
    templateUrl: './edit-device.component.html',
    styleUrls: ['./edit-device.component.scss'],
})
export class EditDeviceComponent implements OnInit {
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

    deviceWorkCopy: Device;
    constructor(
        public deviceService: DeviceService,
        public dialogRef: MatDialogRef<EditDeviceComponent>,
        @Inject(MAT_DIALOG_DATA) public device: Device
    ) {
        this.deviceWorkCopy = {
            uuid: device.uuid,
            name: device.name,
            type: device.type,
            address: device.address,
            port: device.port,
            available: device.available,
            user: device.user,
        };
    }

    ngOnInit(): void {}
}
