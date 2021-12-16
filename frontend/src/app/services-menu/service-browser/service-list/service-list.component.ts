import { Component, OnInit, ViewChild } from '@angular/core';
import {
    animate,
    state,
    style,
    transition,
    trigger,
} from '@angular/animations';

import {
    Service,
    ServiceStatus,
    ServiceUuidList,
} from '@app/_models';
import { ServiceService } from '@app/_services'

import { MatDialog } from '@angular/material/dialog';
import { MatTable } from '@angular/material/table';
// import { ServiceDetailComponent } from '../service-detail/service-detail.component';  // To be included
import { EditServiceComponent } from '../edit-service/edit-service.component';
import { AddServiceComponent } from '../add-service/add-service.component';

interface RowData {
    service: Service;
    status: ServiceStatus;
    detailsLoaded: boolean;
}

@Component({
    selector: 'app-service-list',
    templateUrl: './service-list.component.html',
    styleUrls: ['./service-list.component.scss'],
    animations: [
        trigger('detailExpand', [
            state('collapsed', style({ height: '0px', minHeight: '0' })),
            state('expanded', style({ height: '*' })),
            transition(
                'expanded <=> collapsed',
                animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')
            ),
        ]),
    ],
})
export class ServiceListComponent implements OnInit {
    dataSource: RowData[] = [];
    tableColumns = [
        'name',
        'type',
        'address',
        'port',
        'free',
        'online',
        'status',
        'edit',
    ];
    selected: number | null = null;

    @ViewChild(MatTable) table: MatTable<any>;
    constructor(
        public serviceService: ServiceService,
        public dialog: MatDialog
    ) {}

    async getServices() {
        const serviceList = await this.serviceService.getServiceList();
        const data: RowData[] = [];
        for (const dev of serviceList) {
            data.push({
                service: dev,
                status: { online: false, status: '' },
                detailsLoaded: false,
            });
        }
        this.dataSource = data;
        this.table.renderRows();
        for (let i = 0; i < this.dataSource.length; i++) {
            const promise = this.serviceService.getServiceStatus(
                this.dataSource[i].service.uuid
            );
            promise.then((status) => {
                this.dataSource[i].status = status;
                this.table.renderRows();
            });
        }
    }
    /*
    async getServices() {
        const serviceList = await this.serviceService.getServiceList();
        const data: RowData[] = [];
        for (const dev of serviceList) {
            data.push({
                service: dev,
                status: { online: false, status: '' },
                detailsLoaded: false,
            });
        }
        this.dataSource = data;
        this.table.renderRows();
        // const serviceUuidList: ServiceUuidList = {data: []};
        const serviceUuidList: string[] = [];
        for (let i = 0; i < this.dataSource.length; i++) {
            serviceUuidList.push(
                this.dataSource[i].service.uuid
            );
        }
        const serviceStatusList = await this.serviceService.getServiceStatusList(serviceUuidList);
        console.log('heya');
        console.log(serviceStatusList);
        for (let i = 0; i < this.dataSource.length; i++) {
            this.dataSource[i].status = serviceStatusList.data[i];
        }
        console.log('hoo')
        this.table.renderRows();

        for (let i = 0; i < this.dataSource.length; i++) {
            const promise = this.serviceService.getServiceStatus(
                this.dataSource[i].service.uuid
            );
            await promise.then((status) => {
                this.dataSource[i].status = status;
                this.table.renderRows();
            });
        }

    }
    */
    async add_service() {
        const dialogRef = this.dialog.open(AddServiceComponent, {
            width: '100%',
        });
        const result = await dialogRef.afterClosed().toPromise();
        await this.serviceService.addService(result);
        await this.refresh();
    }
    async add_edge_gateway() {
        // Todo: Create a component for the addition of an edge gateway
        // const dialogRef = this.dialog.open(AddEdgeGatewayComponent, {
        //     width: '100%',
        // });
        // Placeholder
        const dialogRef = this.dialog.open(AddServiceComponent, {
            width: '100%',
        });
        const result = await dialogRef.afterClosed().toPromise();
        // await this.serviceService.addEdgeGateway(result);
        await this.refresh();
    }

    async edit(i: number) {
        const dialogRef = this.dialog.open(EditServiceComponent, {
            data: this.dataSource[i].service,
        });
        const result = await dialogRef.afterClosed().toPromise();
        await this.serviceService.setService(result.uuid, result);
        await this.refresh();
    }

    async delete(i: number) {
        await this.serviceService.deleteService(this.dataSource[i].service.uuid);
        await this.refresh();
    }

    async refresh() {
        await this.getServices();
    }

    expand(i: number) {
        this.selected = this.selected === i ? null : i;
        this.dataSource[i].detailsLoaded = true;
    }

    ngOnInit() {
        this.getServices();
    }
}
