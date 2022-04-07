import { Component, OnInit, Input } from '@angular/core';
import {SilaFeatureInfo} from '../../../_models';

@Component({
    selector: 'app-service-feature',
    templateUrl: './service-feature.component.html',
    styleUrls: ['./service-feature.component.scss'],
})
export class ServiceFeatureComponent implements OnInit {
    @Input()
    feature: SilaFeatureInfo;
    @Input()
    serviceUUID: string;
    expand = false;
    constructor() {}

    ngOnInit(): void {}
}
