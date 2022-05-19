import { Component, OnInit, Input } from '@angular/core';
import {SilaProperty} from '@app/_models';
import {ServiceService} from '@app/_services';
import {Subscription} from 'rxjs';

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
    subscription: Subscription
    isRunning = false;


    constructor(private serviceService: ServiceService) {}

    ngOnInit(): void {
    }

    async getProperty(propertyIdentifier: string) {
        this.returnValues = []

        const result = await this.serviceService.getUnobservableFeaturePropertyResponse(
                this.serviceUUID,
                this.featureIdentifier,
                propertyIdentifier
            )

        this.returnValues.push(result.response[propertyIdentifier])
    }

    async toggleObservable(propertyIdentifier: string) {
        if (this.isRunning) {
            this.isRunning = false
            this.subscription.unsubscribe()
            this.subscription = undefined
            await this.serviceService.deleteObservable(propertyIdentifier)
        }
        else {
            this.isRunning = true
            const result = await this.serviceService.startObservable(
                this.serviceUUID,
                this.featureIdentifier,
                propertyIdentifier
            )

            this.subscription = this.serviceService.createSocket(propertyIdentifier, result).subscribe(
                data => {
                    const parsedResponse = JSON.parse(data as string)

                    this.returnValues[0] = parsedResponse[result].property_response.property_responses
                })
        }
    }
}
