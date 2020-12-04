import {
    Component,
    OnInit,
    Input,
    OnChanges,
    SimpleChanges,
} from '@angular/core';
import {Device, DeviceCommand, DeviceService, DeviceStatus} from '../device.service';
import {DatabaseService, CheckboxParam} from '../database.service';
export interface CustomPollingInterval {
    duration: number;
}

@Component({
  selector: 'app-data-handler-device-command',
  templateUrl: './data-handler-device-command.component.html',
  styleUrls: ['./data-handler-device-command.component.scss']
})


export class DataHandlerDeviceCommandComponent implements OnInit, OnChanges {
    @Input()
    command: DeviceCommand;
    @Input()
    featureIdentifier: string;
    @Input()
    uuid: string;
    paramValues: string[] = [];
    expand = false;
    checkboxes: CheckboxParam[] = [];
    dataTransferCheckbox = false; // Delete once properly implemented
    metaDataCheckbox = false;  // Delete once properly implemented
    defaultPollingInterval = 60;
    customPollingInterval: CustomPollingInterval;

  constructor(private databaseService: DatabaseService) {}
    ngOnChanges(changes: SimpleChanges) {
        for (const param of this.command.parameters) {
            this.paramValues.push('');
        }
        // Update and send changes of checkboxes to backend
    }

    ngOnInit(): void {
        // Get all checkbox vakues for all commands on init
        // this.checkboxes = this.databaseService.getCheckboxInfoCommand(this.uuid, this.featureIdentifier, this.command);
    }

}
