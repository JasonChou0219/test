import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import {EditSilaServiceInfo, Service, ServiceInfo, SilaServiceInfo} from '@app/_models';
import { ServiceService } from '@app/_services'
import { identifierModuleUrl } from '@angular/compiler';

@Component({
    selector: 'app-edit-service',
    templateUrl: './edit-service.component.html',
    styleUrls: ['./edit-service.component.scss'],
})
export class EditServiceComponent implements OnInit {
    serviceWorkCopy: EditSilaServiceInfo;
    constructor(
        public serviceService: ServiceService,
        public dialogRef: MatDialogRef<EditServiceComponent>,
        @Inject(MAT_DIALOG_DATA) public service: SilaServiceInfo
    ) {
        this.serviceWorkCopy = {
            name: service.name,
            parsed_ip_address: service.parsed_ip_address,
            port: service.port
        };
    }

    ngOnInit(): void {}
}
