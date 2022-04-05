import { Component, OnInit} from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import {AddSilaServiceInfo} from '@app/_models';
import { ServiceService } from '@app/_services'

@Component({
    selector: 'app-add-service',
    templateUrl: './add-service.component.html',
    styleUrls: ['./add-service.component.scss'],
})
export class AddServiceComponent implements OnInit {
    dataSource = [];
    tableColumns = ['address', 'port'];

    discoveryStarted = false;
    serviceWorkCopy: AddSilaServiceInfo;
    constructor(
        public serviceService: ServiceService,
        public dialogRef: MatDialogRef<AddServiceComponent>
    ) {
        this.serviceWorkCopy = {
            parsed_ip_address: '',
            port: 50052,
            encrypted: false
        };
    }
    toggleEncrypted(){
        this.serviceWorkCopy.encrypted = !this.serviceWorkCopy.encrypted
    }

    ngOnInit(): void {}
}
