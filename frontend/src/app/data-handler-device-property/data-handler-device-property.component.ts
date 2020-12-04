import {Component, Input, OnInit, SimpleChanges} from '@angular/core';
import { DeviceProperty } from '../device.service';
import {CheckboxParam, DatabaseService} from "../database.service";
// import {CustomPollingInterval} from '../data-handler-device-feature/data-handler-device-feature.component';

export interface CustomPollingInterval {
    duration: number;
}

@Component({
  selector: 'app-data-handler-device-property',
  templateUrl: './data-handler-device-property.component.html',
  styleUrls: ['./data-handler-device-property.component.scss']
})
export class DataHandlerDevicePropertyComponent implements OnInit {
    @Input()
    property: DeviceProperty;
    @Input()
    featureIdentifier: string;
    @Input()
    uuid: string;
    execute = '';
    expand = false;
    checkboxes: CheckboxParam[] = [];
    dataTransferCheckbox = false;  // Delete once properly implemented
    metaDataCheckbox = false;  // Delete once properly implemented
    defaultPollingInterval = 60;
    customPollingInterval: CustomPollingInterval;

    constructor(private databaseService: DatabaseService) {}
    // ngOnChanges(changes: SimpleChanges) {
        // Update and send changes of checkboxes to backend
    //    }

    ngOnInit(): void {
        // Get all checkbox vakues for all commands on init
        // this.checkboxes = this.databaseService.getCheckboxInfoProperty(this.uuid, this.featureIdentifier, this.property);
    }

}
