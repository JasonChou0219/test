import { Component, OnInit, Input } from '@angular/core';
import {DeviceProperty, DeviceService, FeaturePropertyResult} from '../device.service';

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
    returnValues: FeaturePropertyResult[] = [];
    execute = '';
    expand = false;

    constructor(private deviceService: DeviceService) {}

    ngOnInit(): void {}

    async getProperty(name: string) {
        console.log(
            this.returnValues = await this.deviceService.getFeatureProperty(
                this.deviceUUID,
                this.featureIdentifier,
                name
            )
        );
        console.log(this.returnValues.find(item => item.name === name.toLowerCase()).value);
    }
}
