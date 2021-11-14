import { Component, OnInit, Input } from '@angular/core';
import { ServiceFeature } from '../service.service';

@Component({
    selector: 'app-service-feature',
    templateUrl: './service-feature.component.html',
    styleUrls: ['./service-feature.component.scss'],
})
export class ServiceFeatureComponent implements OnInit {
    @Input()
    feature: ServiceFeature;
    @Input()
    serviceUUID: string;
    expand = false;
    constructor() {}

    ngOnInit(): void {}
}
