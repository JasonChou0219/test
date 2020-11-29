import { Component, OnInit, Input } from '@angular/core';
import { DeviceProperty, DeviceService } from '../device.service';

@Component({
    selector: 'app-device-property',
    templateUrl: './device-property.component.html',
    styleUrls: ['./device-property.component.scss'],
})
export class DevicePropertyComponent implements OnInit {
    @Input()
    property: DeviceProperty;
    @Input()
    featureIdentifier: string;
    @Input()
    deviceUUID: string;
    execute = '';
    expand = false;

    constructor(private deviceService: DeviceService) {}

    ngOnInit(): void {}

    getProperty(name: string) {
        console.log(
            this.deviceService.getFeatureProperty(
                this.deviceUUID,
                this.featureIdentifier,
                name
            )
        );
    }
}
