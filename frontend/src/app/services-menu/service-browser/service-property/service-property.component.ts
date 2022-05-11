import { Component, OnInit, Input } from '@angular/core';
import {SilaProperty} from '@app/_models';
import {ServiceService} from '@app/_services';

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
    returnValues = [];
    execute = '';
    expand = false;

    constructor(private serviceService: ServiceService) {}

    ngOnInit(): void {
    }

    async getProperty(propertyIdentifier: string) {
           const result = await this.serviceService.getFeaturePropertyResponse(
                this.serviceUUID,
                this.featureIdentifier,
                propertyIdentifier
            )

           this.returnValues.push(result.response[propertyIdentifier])
    }
}
