import {Component, Input, OnInit} from '@angular/core';
import { DeviceProperty } from '../device.service';
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
    execute = '';
    expand = false;
    dataTransferCheckbox = false;
    metaDataCheckbox = false;
    defaultPollingInterval = 60;
    customPollingInterval: CustomPollingInterval;
  constructor() { }

  ngOnInit(): void {
  }

}
