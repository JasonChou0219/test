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
    featureId: number;
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
  async setCheckboxCommandLevel(uuid: string, featureId: number, commandId: number, meta: boolean,
                                active: boolean, metaInterval: number, nonMetaInterval: number) {
        await this.databaseService.setCheckboxCommandLevel(uuid, featureId, commandId,
            meta, active, metaInterval, nonMetaInterval);
        // Maybe I need to refresh here,but hopefully the two-way binding works...
        // Maybe I should just pass the commandInterface
  }
    ngOnChanges(changes: SimpleChanges) {
        for (const param of this.command.parameters) {
            this.paramValues.push('');
        }
        // Update and send changes of checkboxes to backend
    }

    ngOnInit(): void {
    }

}
