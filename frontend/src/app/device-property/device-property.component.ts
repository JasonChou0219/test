import { Component, OnInit, Input } from '@angular/core';
import { DeviceProperty } from '../device.service';

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
    execute = '';
    expand = false;

    constructor() {}

    ngOnInit(): void {}
}
