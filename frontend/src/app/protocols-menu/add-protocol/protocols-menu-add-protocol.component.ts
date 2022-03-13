import { Component, OnInit } from '@angular/core';
import {
    ProtocolInfo,
    ProtocolParameterInfo,
    ProtocolResponseInfo,
    Service,
    ServiceCommand,
    ServiceFeature,
    ServiceProperty
} from '@app/_models';
import { ProtocolService, ServiceService } from '@app/_services';

@Component({
    selector: 'app-protocols-menu-add-protocol',
    templateUrl: './protocols-menu-add-protocol.component.html',
    styleUrls: ['./protocols-menu-add-protocol.component.scss']
})
export class ProtocolsMenuAddProtocolComponent implements OnInit {
    protocolInfo: ProtocolInfo;
    services: Service[];
    selectedService: Service;
    availableFeatures: ServiceFeature[];

    selectedFeatureForCommand: ServiceFeature;
    selectedCommand: ServiceCommand;

    selectedFeatureForProperty: ServiceFeature;
    selectedProperty: ServiceProperty;

    constructor(
        public serviceService: ServiceService,
        public protocolService: ProtocolService,
    ) {
        this.protocolInfo = {
            title: '',
            service: {uuid: undefined,
                      features: []},
        };
    }

    async getServices() {
        this.services = await this.serviceService.getServiceList();
    }

    ngOnInit(): void {
        this.getServices();
    }

    async createProtocol() {
        await this.protocolService.createProtocol(this.protocolInfo);
        console.log('createProtocol');
    }

    async selectService() {
        this.availableFeatures = await this.serviceService.getServiceFeatures(this.selectedService.service_uuid);
        this.protocolInfo.service = {
            uuid: this.selectedService.service_uuid,
            features: [],
        }
    }

    addCommand() {
        let indexOfFeature: number;
        this.protocolInfo.service.features.forEach((value, index) => {
            if (value.identifier === this.selectedFeatureForCommand.identifier) {
                indexOfFeature = index;
            }
        })

        const parameters: ProtocolParameterInfo[] = [];
        this.selectedCommand.parameters.forEach((value) => {
            parameters.push({
                identifier: value.identifier,
                value: '',
            })
        })

        const responses: ProtocolResponseInfo[] = [];
        this.selectedCommand.responses.forEach((value) => {
            responses.push({
                identifier: value.identifier,
            })
        })

        if (indexOfFeature === undefined) {
            this.protocolInfo.service.features.push({
                identifier: this.selectedFeatureForCommand.identifier,
                commands: [{
                    identifier: this.selectedCommand.identifier,
                    observable: this.selectedCommand.observable,
                    meta: false,
                    interval: 1,
                    parameters: parameters,
                    responses: responses,
                }],
                properties: [],
            })
        }
        else {
            this.protocolInfo.service.features[indexOfFeature].commands.push({
                identifier: this.selectedCommand.identifier,
                observable: this.selectedCommand.observable,
                meta: false,
                interval: 1,
                parameters: parameters,
                responses: responses,
            })
        }
        this.selectedFeatureForCommand = undefined;
        this.selectedCommand = undefined;
    }

    addProperty() {
        let indexOfFeature: number;
        this.protocolInfo.service.features.forEach((value, index) => {
            if (value.identifier === this.selectedFeatureForProperty.identifier) {
                indexOfFeature = index;
            }
        })

        if (indexOfFeature === undefined) {
            this.protocolInfo.service.features.push({
                identifier: this.selectedFeatureForProperty.identifier,
                properties: [{
                    identifier: this.selectedProperty.identifier,
                    observable: this.selectedProperty.observable,
                    meta: false,
                    interval: 1,
                }],
                commands: [],
            })
        }
        else {
            this.protocolInfo.service.features[indexOfFeature].properties.push({
                identifier: this.selectedProperty.identifier,
                observable: this.selectedProperty.observable,
                meta: false,
                interval: 1,
            })
        }
        this.selectedFeatureForProperty = undefined;
        this.selectedProperty = undefined;
    }
}
