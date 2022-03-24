import {Component, OnInit, ViewChild} from '@angular/core';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {MatTable} from '@angular/material/table';
import {ServiceService} from '@app/_services';
import {MatDialog} from '@angular/material/dialog';
import {SilaServiceInfo} from '@app/_models';


interface RowData {
    service: SilaServiceInfo;
    detailsLoaded: boolean;
}


@Component({
  selector: 'app-discover-service',
  templateUrl: './discover-service.component.html',
  styleUrls: ['./discover-service.component.scss'],
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
export class DiscoverServiceComponent implements OnInit {

    dataSource: RowData[] = [];
    tableColumns = [
        'name',
        'type',
        'address',
        'port',
        'connect',
    ];
    selected: number | null = null;

    @ViewChild(MatTable) table: MatTable<any>;
    constructor(
        public serviceService: ServiceService,
        public dialog: MatDialog
    ) {}

    async getServices() {
        const serviceList = await this.serviceService.discoverServiceMDNS();
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

    async refresh() {
        await this.getServices();
    }

    ngOnInit() {
        this.getServices();
    }

}
