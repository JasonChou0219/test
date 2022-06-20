import { Component, OnInit } from '@angular/core';
import {
    ProtocolInfo,
    ProtocolParameterInfo,
    ProtocolResponseInfo,
    Service,
    ServiceCommand,
    ServiceFeature,
    ServiceProperty, SilaFeatureInfo, SilaServiceInfo
} from '@app/_models';
import { ProtocolService, ServiceService } from '@app/_services';
import { Router } from '@angular/router';

@Component({
    selector: 'app-protocols-menu-add-protocol',
    templateUrl: './protocols-menu-add-protocol.component.html',
    styleUrls: ['./protocols-menu-add-protocol.component.scss']
})
export class ProtocolsMenuAddProtocolComponent implements OnInit {
    protocolInfo: ProtocolInfo;
    services: SilaServiceInfo[];
    selectedService: SilaServiceInfo;
    availableFeatures: SilaFeatureInfo[];

    selectedFeatureForCommand: ServiceFeature;
    selectedCommand: ServiceCommand;

    selectedFeatureForProperty: ServiceFeature;
    selectedProperty: ServiceProperty;

    customDataKey: string;
    customDataValue: string;

    constructor(
        public serviceService: ServiceService,
        public protocolService: ProtocolService,
        private router: Router,
    ) {
        this.protocolInfo = {
            title: '',
            service: {uuid: undefined,
                      features: []},
            custom_data: {},
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
        this.router.navigate(['/dashboard/protocols']);
    }

    cancel() {
        this.router.navigate(['/dashboard/protocols']);
    }

    async selectService() {
        this.availableFeatures = await this.serviceService.browseFeatureDefinitions(this.selectedService.uuid);
        this.protocolInfo.service = {
            uuid: this.selectedService.uuid,
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
                    parameters,
                    responses,
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
                parameters,
                responses,
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

    addCustomData() {
        this.protocolInfo.custom_data[this.customDataKey] = this.customDataValue;
        this.customDataKey = undefined;
        this.customDataValue = undefined;
    }

    deleteCommand(featureIndex: number, commandIndex: number) {
        this.protocolInfo.service.features[featureIndex].commands.splice(commandIndex, 1);
        if (this.protocolInfo.service.features[featureIndex].commands.length === 0
            && this.protocolInfo.service.features[featureIndex].properties.length === 0) {
            this.protocolInfo.service.features.splice(featureIndex, 1);
        }
    }

    deleteProperty(featureIndex: number, propertyIndex: number) {
        this.protocolInfo.service.features[featureIndex].properties.splice(propertyIndex, 1);
        if (this.protocolInfo.service.features[featureIndex].commands.length === 0
            && this.protocolInfo.service.features[featureIndex].properties.length === 0) {
            this.protocolInfo.service.features.splice(featureIndex, 1);
        }
    }

    deleteCustomData(key: string) {
        delete this.protocolInfo.custom_data[key]
    }
}
