import {Component, Input, OnInit} from '@angular/core';
import { DeviceFeature } from '../device.service';

@Component({
  selector: 'app-data-handler-device-feature',
  templateUrl: './data-handler-device-feature.component.html',
  styleUrls: ['./data-handler-device-feature.component.scss']
})
export class DataHandlerDeviceFeatureComponent implements OnInit {
    @Input()
    feature: DeviceFeature;
    @Input()
    uuid: string;
    expand = false;
  constructor() { }

  ngOnInit(): void {
  }

}
