import { Component, OnInit, Input } from '@angular/core';
import {
    Service,
    ServiceService,
    ServiceFeature,
    ServiceCommand,
    ServiceProperty,
    ServiceParameter,
} from '../service.service';
import { NestedTreeControl } from '@angular/cdk/tree';
import { MatTreeNestedDataSource } from '@angular/material/tree';

interface TreeNode {
    name: string;
    value?: string;
    children?: TreeNode[];
}
function buildParameterTree(parameter: ServiceParameter): TreeNode[] {
    const nodes: TreeNode[] = [];
    nodes.push({ name: 'Identifier', value: parameter.identifier });
    nodes.push({ name: 'Description', value: parameter.description });
    nodes.push({ name: 'Type', value: parameter.data_type });
    return nodes;
}

function buildPropertyTree(property: ServiceProperty): TreeNode[] {
    const nodes: TreeNode[] = [];
    nodes.push({ name: 'Identifier', value: property.identifier });
    nodes.push({ name: 'Description', value: property.description });
    // const responseChilds: TreeNode[] = [];
    // responseChilds.push({
    //        name: property.response.name,
    //        children: buildParameterTree(property.response),
    //    });
    nodes.push({
        name: 'Response',
        children: buildParameterTree(property.response),
    });
    return nodes;
}

function buildCommandTree(command: ServiceCommand): TreeNode[] {
    const nodes: TreeNode[] = [];
    nodes.push({ name: 'Identifier', value: command.identifier });
    nodes.push({ name: 'Description', value: command.description });
    const parameterChilds: TreeNode[] = [];
    for (const parameter of command.parameters) {
        if (parameter.identifier !== 'EmptyParameter') {
            parameterChilds.push({
                name: parameter.display_name,
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
            name: response.display_name,
            children: buildParameterTree(response),
        });
    }
    nodes.push({ name: 'Responses', children: responseChilds });
    return nodes;
}

function buildFeatureTree(feature: ServiceFeature): TreeNode[] {
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

function buildFeaturesTree(features: ServiceFeature[]): TreeNode[] {
    const nodes: TreeNode[] = [];
    for (const feature of features) {
        nodes.push({ name: feature.name, children: buildFeatureTree(feature) });
    }
    return nodes;
}

@Component({
    selector: 'app-service-detail',
    templateUrl: './service-detail.component.html',
    styleUrls: ['./service-detail.component.scss'],
})
export class ServiceDetailComponent implements OnInit {
    @Input() service: Service;
    treeControl = new NestedTreeControl<TreeNode>((node) => node.children);
    dataSource = new MatTreeNestedDataSource<TreeNode>();
    features: ServiceFeature[] = [];
    constructor(public serviceService: ServiceService) {}

    async getFeatures() {
        this.features = await this.serviceService.getServiceFeatures(
            this.service.uuid
        );
        // this.dataSource.data = buildFeaturesTree(this.features);
    }

    hasChild = (_: number, node: TreeNode) =>
        !!node.children && node.children.length > 0;

    ngOnInit(): void {
        this.getFeatures();
    }
}
