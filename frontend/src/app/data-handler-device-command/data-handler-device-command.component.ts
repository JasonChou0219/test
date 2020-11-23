import {
    Component,
    OnInit,
    Input,
    OnChanges,
    SimpleChanges,
} from '@angular/core';
import {Device, DeviceCommand, DeviceStatus} from '../device.service';

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
    paramValues: string[] = [];
    expand = false;
    dataTransferCheckbox = false;
    metaDataCheckbox = false;
    defaultPollingInterval = 60;
    customPollingInterval: CustomPollingInterval;
  constructor() {}
    ngOnChanges(changes: SimpleChanges) {
        for (const param of this.command.parameters) {
            this.paramValues.push('');
        }
    }

    ngOnInit(): void {}

}
