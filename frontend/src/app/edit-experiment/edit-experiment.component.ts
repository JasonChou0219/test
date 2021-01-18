import {Component, Inject, OnInit, ViewChild} from '@angular/core';
import {Device, DeviceService, Experiment, ScriptInfo} from '../device.service';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {format} from 'date-fns';

@Component({
    selector: 'app-edit-experiment',
    templateUrl: './edit-experiment.component.html',
    styleUrls: ['./edit-experiment.component.scss']
})
export class EditExperimentComponent implements OnInit {

    experimentInfo;
    scripts: ScriptInfo[] = [];
    devices: Device[] = [];
    @ViewChild('devs')
    deviceList;
    constructor(
        private deviceService: DeviceService,
        public dialogRef: MatDialogRef<EditExperimentComponent>,
        @Inject(MAT_DIALOG_DATA) public experiment: Experiment
    ) {
        let time = new Date(0);
        time.setUTCSeconds(experiment.start);
        const startDate = format(
            time,
            'dd.MM.yyyy HH:mm'
        );
        time = new Date(0);
        time.setUTCSeconds(experiment.end);
        const endDate = format(
            time,
            'dd.MM.yyyy HH:mm'
        );
        this.experimentInfo = {
            id: experiment.id,
            name: experiment.name,
            start: startDate,
            end: endDate,
            user: experiment.user,
            deviceBookings: this.experiment.deviceBookings,
            devices: [],
            scriptID: experiment.scriptID,
            scriptName: experiment.scriptName
        };
    }
    compareFunction(device: Device) {
        const deviceListBooked = [];
        this.experimentInfo.deviceBookings.map(({ deviceName }) => (deviceListBooked.push(deviceName)));
        if (deviceListBooked.length > 0) {
            return deviceListBooked.includes(device.name);
        }
        else {
            return false;
        }
    }
    // = (o1: any, o2: any) => o1.id === o2.id;
    edit() {
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
