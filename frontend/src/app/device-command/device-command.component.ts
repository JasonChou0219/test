import {
    Component,
    OnInit,
    Input,
    OnChanges,
    SimpleChanges,
} from '@angular/core';
import { DeviceCommand } from '../device.service';

@Component({
    selector: 'app-device-command',
    templateUrl: './device-command.component.html',
    styleUrls: ['./device-command.component.scss'],
})
export class DeviceCommandComponent implements OnInit, OnChanges {
    @Input()
    command: DeviceCommand;
    @Input()
    featureIdentifier: string;
    @Input()
    deviceUUID: string;
    paramValues: string[] = [];
    expand = false;

    constructor() {}

    ngOnChanges(changes: SimpleChanges) {
        for (const param of this.command.parameters) {
            this.paramValues.push('');
        }
    }

    ngOnInit(): void {}
}
