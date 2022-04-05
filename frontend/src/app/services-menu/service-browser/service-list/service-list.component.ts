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
    ServiceUuidList, SilaServiceInfo,
} from '@app/_models';
import { ServiceService } from '@app/_services'

import { MatDialog } from '@angular/material/dialog';
import { MatTable } from '@angular/material/table';
// import { ServiceDetailComponent } from '../service-detail/service-detail.component';  // To be included
import { EditServiceComponent } from '../edit-service/edit-service.component';
import { AddServiceComponent } from '../add-service/add-service.component';

interface RowData {
    service: SilaServiceInfo;
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
        'online',
        'isGateway',
        'toggleConnection',
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
                detailsLoaded: false,
            });
        }
        this.dataSource = data;
        this.table.renderRows();
    }

    async add_service() {
        const dialogRef = this.dialog.  open(AddServiceComponent, {
            width: '100%',
        });
        const result = await dialogRef.afterClosed().toPromise();
        if (result){
            await this.serviceService.connectService(result.parsed_ip_address, result.port, result.encrypted)
            await this.refresh();
        }
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
        if (result){
            await this.serviceService.updateServiceInfo(this.dataSource[i].service.uuid, JSON.stringify(result))
            await this.refresh();
        }
    }

    async delete(i: number) {
        await this.serviceService.deleteServiceInfo(this.dataSource[i].service.uuid);
        await this.refresh();
    }

    async refresh() {
        await this.getServices();
    }

    expand(i: number) {
        this.selected = this.selected === i ? null : i;
        this.dataSource[i].detailsLoaded = true;
    }

    async toggleFavourite(i: number) {
        const service = this.dataSource[i].service
        const fav =  !service.favourite
        const body = {"favourite": fav}
        await this.serviceService.updateServiceInfo(service.uuid, body);
        await this.refresh();
    }

    async toggleConnection(i: number) {
        const service = this.dataSource[i].service
        const connected =  service.connected

        if (connected){
            await this.serviceService.disconnectService(service.uuid);
        }
        else {
            await this.serviceService.connectService(service.parsed_ip_address, service.port);
        }
        await this.refresh();
    }

    ngOnInit() {
        this.getServices();
    }
}
