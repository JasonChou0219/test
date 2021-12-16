import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Service } from '@app/_models';
import { ServiceService } from '@app/_services'
import { identifierModuleUrl } from '@angular/compiler';

@Component({
    selector: 'app-edit-service',
    templateUrl: './edit-service.component.html',
    styleUrls: ['./edit-service.component.scss'],
})
export class EditServiceComponent implements OnInit {
    /* serviceTypes = [
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
    serviceWorkCopy: Service;
    constructor(
        public serviceService: ServiceService,
        public dialogRef: MatDialogRef<EditServiceComponent>,
        @Inject(MAT_DIALOG_DATA) public service: Service
    ) {
        this.serviceWorkCopy = {
            uuid: service.uuid,
            server_uuid: service.server_uuid,
            name: service.name,
            type: service.type,
            address: service.address,
            port: service.port,
            available: service.available,
            user: service.user,
            databaseId: service.databaseId,
            dataHandlerActive: service.dataHandlerActive,
        };
    }

    ngOnInit(): void {}
}
