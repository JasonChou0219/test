import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { Script, ScriptInfo, Device, DeviceService } from '../device.service';
import { format } from 'date-fns';

@Component({
    selector: 'app-add-job',
    templateUrl: './add-experiment.component.html',
    styleUrls: ['./add-experiment.component.scss'],
})
export class AddExperimentComponent implements OnInit {
    experimentInfo;
    scripts: ScriptInfo[] = [];
    devices: Device[] = [];
    @ViewChild('devs')
    deviceList;
    constructor(
        private deviceService: DeviceService,
        public dialogRef: MatDialogRef<AddExperimentComponent>
    ) {
        const now = new Date();
        const today = now.getDate();
        const startDate = format(now, 'dd.MM.yyyy HH:mm');
        const endDate = format(
            new Date(now).setDate(today + 2),
            'dd.MM.yyyy HH:mm'
        );
        this.experimentInfo = {
            name: '',
            start: startDate,
            end: endDate,
            devices: [],
            script: -1,
        };
    }

    add() {
        this.experimentInfo.devices = this.deviceList.selectedOptions.selected.map(
            (device) => {
                return device.value.uuid;
            }
        );
    }
    async ngOnInit() {
        this.scripts = await this.deviceService.getUserScriptsInfo();
        this.devices = await this.deviceService.getDeviceList();
    }
}
