import {Component, Input, OnInit} from '@angular/core';
import {
    Device,
    DeviceService,
    DeviceFeature,
    DeviceCommand,
    DeviceProperty,
    DeviceParameter,
} from '../device.service';
import { NestedTreeControl } from '@angular/cdk/tree';
import { MatTreeNestedDataSource } from '@angular/material/tree';

interface TreeNode {
    name: string;
    value?: string;
    children?: TreeNode[];
}
function buildParameterTree(parameter: DeviceParameter): TreeNode[] {
    const nodes: TreeNode[] = [];
    nodes.push({ name: 'Identifier', value: parameter.identifier });
    nodes.push({ name: 'Description', value: parameter.description });
    nodes.push({ name: 'Type', value: parameter.type });
    return nodes;
}

function buildPropertyTree(property: DeviceProperty): TreeNode[] {
    const nodes: TreeNode[] = [];
    nodes.push({ name: 'Identifier', value: property.identifier });
    nodes.push({ name: 'Description', value: property.description });
    const responseChilds: TreeNode[] = [];
    responseChilds.push({
            name: property.response.name,
            children: buildParameterTree(property.response),
        });
    nodes.push({ name: 'Responses', children: responseChilds });
    return nodes;
}

function buildCommandTree(command: DeviceCommand): TreeNode[] {
    const nodes: TreeNode[] = [];
    nodes.push({ name: 'Identifier', value: command.identifier });
    nodes.push({ name: 'Description', value: command.description });
    const parameterChilds: TreeNode[] = [];
    for (const parameter of command.parameters) {
        if (parameter.identifier !== 'EmptyParameter') {
            parameterChilds.push({
                name: parameter.name,
                children: buildParameterTree(parameter),
            });
        }
    }
    if (parameterChilds.length > 0) {
        nodes.push({ name: 'Parameters', children: parameterChilds });
    } else {
        nodes.push({ name: 'Parameters', value: 'Nothing' });
    }
    const responseChilds: TreeNode[] = [];
    for (const response of command.responses) {
        responseChilds.push({
            name: response.name,
            children: buildParameterTree(response),
        });
    }
    nodes.push({ name: 'Responses', children: responseChilds });
    return nodes;
}

function buildFeatureTree(feature: DeviceFeature): TreeNode[] {
    const nodes: TreeNode[] = [];
    nodes.push({ name: 'Identifier', value: feature.identifier });
    nodes.push({ name: 'Description', value: feature.description });
    nodes.push({ name: 'Version', value: feature.feature_version });
    const commandChilds: TreeNode[] = [];
    for (const command of feature.commands) {
        commandChilds.push({
            name: command.name,
            children: buildCommandTree(command),
        });
    }
    nodes.push({ name: 'Commands', children: commandChilds });
    if (feature.properties.length > 0) {
        const propertyChilds: TreeNode[] = [];
        for (const property of feature.properties) {
            propertyChilds.push({
                name: property.name,
                children: buildPropertyTree(property),
            });
        }
        nodes.push({ name: 'Properties', children: propertyChilds });
    } else {
        nodes.push({ name: 'Properties', value: 'Nothing' });
    }
    return nodes;
}

function buildFeaturesTree(features: DeviceFeature[]): TreeNode[] {
    const nodes: TreeNode[] = [];
    for (const feature of features) {
        nodes.push({ name: feature.name, children: buildFeatureTree(feature) });
    }
    return nodes;
}

@Component({
  selector: 'app-data-handler-device-detail',
  templateUrl: './data-handler-device-detail.component.html',
  styleUrls: ['./data-handler-device-detail.component.scss']
})
export class DataHandlerDeviceDetailComponent implements OnInit {
    @Input() device: Device;
    treeControl = new NestedTreeControl<TreeNode>((node) => node.children);
    dataSource = new MatTreeNestedDataSource<TreeNode>();
    features: DeviceFeature[] = [];
    dataTransferCheckbox = false;
    metaDataCheckbox = false;

    constructor(public deviceService: DeviceService) {}
    async getFeatures() {
        this.features = await this.deviceService.getDeviceFeatures(
            this.device.uuid
        );
        // this.dataSource.data = buildFeaturesTree(this.features);
    }
    hasChild = (_: number, node: TreeNode) =>
        !!node.children && node.children.length > 0;
    ngOnInit(): void {
        this.getFeatures();
    }

}
