import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { DeviceService, Device } from '../device.service';
import { format, parse, isValid } from 'date-fns';

@Component({
    selector: 'app-add-booking',
    templateUrl: './add-booking.component.html',
    styleUrls: ['./add-booking.component.scss'],
})
export class AddBookingComponent implements OnInit {
    bookingInfo;
    devices: Device[] = [];
    constructor(
        public deviceService: DeviceService,
        public dialogRef: MatDialogRef<AddBookingComponent>
    ) {}

    async ngOnInit() {
        this.devices = await this.deviceService.getDeviceList();
        const now = format(new Date(), 'dd.MM.yyyy HH:mm');
        this.bookingInfo = {
            name: '',
            start: now,
            end: now,
            device: '',
        };
    }
}
