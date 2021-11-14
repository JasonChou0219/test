import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { Service } from '@app/_models';
import { ServiceService } from '@app/_services'

@Component({
    selector: 'app-add-service',
    templateUrl: './add-service.component.html',
    styleUrls: ['./add-service.component.scss'],
})
export class AddServiceComponent implements OnInit {
    /*
    serviceTypes = [
        {
            value: ServiceType.SILA,
            name: this.serviceService.serviceTypeAsName(ServiceType.SILA),
        },
        {
            value: ServiceType.CUSTOM,
            name: this.serviceService.serviceTypeAsName(ServiceType.CUSTOM),
        },
        {
            value: ServiceType.SOFT,
            name: this.serviceService.serviceTypeAsName(ServiceType.SOFT),
        },
    ];
    */
    serviceTypes = [
        {
            value: 'SiLA 2',
            name: 'SiLA2',
        },
        {
            value: 'LADS',
            name: 'OPC-UA',
        },
        {
            value: 'Magic Unicorn',
            name: 'Rainbow Unicorn',
        },
    ];
    dataSource = [];
    tableColumns = ['name', 'uuid', 'address', 'port', 'hostname', 'select'];

    discoveryStarted = false;
    service: Service;
    constructor(
        public serviceService: ServiceService,
        public dialogRef: MatDialogRef<AddServiceComponent>
    ) {
        this.service = {
            uuid: '',
            server_uuid: '',
            name: '',
            type: '',  // ServiceType.SILA,
            address: '',
            port: 50001,
            available: true,
            dataHandlerActive: false,
        };
    }
    select(i: number) {
        this.service.server_uuid = this.dataSource[i].uuid;
        this.service.name = this.dataSource[i].name;
        this.service.address = this.dataSource[i].ip;
        this.service.port = this.dataSource[i].port;
    }
    async discovery() {
        this.discoveryStarted = true;
        this.dataSource = await this.serviceService.discoverSilaServices();
    }

    ngOnInit(): void {}
}
