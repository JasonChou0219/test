import { Component, OnInit, Input } from '@angular/core';
import { DeviceFeature } from '../device.service';

@Component({
    selector: 'app-device-feature',
    templateUrl: './device-feature.component.html',
    styleUrls: ['./device-feature.component.scss'],
})
export class DeviceFeatureComponent implements OnInit {
    @Input()
    feature: DeviceFeature;
    expand = false;
    constructor() {}

    ngOnInit(): void {}
}
