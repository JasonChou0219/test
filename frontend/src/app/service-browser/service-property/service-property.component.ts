import { Component, OnInit, Input } from '@angular/core';
import {ServiceProperty, ServiceService, FeaturePropertyResult} from '../service.service';

@Component({
    selector: 'app-service-property',
    templateUrl: './service-property.component.html',
    styleUrls: ['./service-property.component.scss'],
})
export class ServicePropertyComponent implements OnInit {
    @Input()
    property: ServiceProperty;
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
    returnValues: FeaturePropertyResult[] = [];
    execute = '';
    expand = false;

    constructor(private serviceService: ServiceService) {}

    ngOnInit(): void {
        this.returnValues = [{
            name: 'test_name',
            value: '[None]',
        }];
    }

    async getProperty(name: string) {
        console.log('testing 1',
            this.returnValues = await this.serviceService.getFeatureProperty(
                this.serviceUUID,
                this.featureOriginator,
                this.featureCategory,
                this.featureIdentifier,
                this.featureVersionMajor,
                name
            )
        );
        console.log(this.returnValues);
        console.log(this.returnValues.find(item => item.name === name.toLowerCase()).value);
    }
}
