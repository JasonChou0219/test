import { Component, OnInit, Input } from '@angular/core';
import {SilaProperty} from '@app/_models';

@Component({
    selector: 'app-service-property',
    templateUrl: './service-property.component.html',
    styleUrls: ['./service-property.component.scss'],
})
export class ServicePropertyComponent implements OnInit {
    @Input()
    property: SilaProperty;
    @Input()
    featureIdentifier: string;
    @Input()
    featureOriginator: string;
    @Input()
    featureCategory: string;
    @Input()
    featureVersionMajor: number;
    @Input()
    serviceUUID: string;
    returnValues: [] = [];
    execute = '';
    expand = false;
    ngOnInit(): void {
    }
}
