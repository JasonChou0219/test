import {
    Component,
    OnInit,
    Input,
    OnChanges,
    SimpleChanges,
} from '@angular/core';
import {DeviceCommand, DeviceService} from '../device.service';

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

    constructor(private deviceService: DeviceService) {}

    ngOnChanges(changes: SimpleChanges) {
        for (const param of this.command.parameters) {
            this.paramValues.push('');
        }
    }

    ngOnInit(): void {}

    callCommand(name: string) {
        console.log(
            // this.deviceService.callFeatureCommand(
            //    this.deviceUUID,
            //    this.featureIdentifier,
            //    name
            //    map of this command.parameter.identifier and respective this.paramValues
            // )
        );
    }
}
