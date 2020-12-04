import {
    Component,
    OnInit,
    Input,
    OnChanges,
    SimpleChanges,
} from '@angular/core';
import {
    DeviceCommand,
    DeviceService,
    FeatureCommandParam, FeatureCommandResult,
} from '../device.service';

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
    paramValues: FeatureCommandParam[] = [];
    returnValues: FeatureCommandResult[] = [];
    expand = false;

    constructor(private deviceService: DeviceService) {}

    ngOnChanges(hanges: SimpleChanges) {
        /*for (const param of this.command.parameters) {
            this.paramValues.push('');
        }
        */
        this.paramValues = this.command.parameters.map((param) => {
            return { name: param.identifier.toLowerCase() + '/' + param.type.toLowerCase(), value: '' };
        });
        console.log(this.paramValues);
    }

    ngOnInit(): void {
        this.returnValues = [{
            name: 'test_name',
            value: '[None] press run!',
        }];
    }

    async callCommand(name: string) {
        console.log(
            this.returnValues = await this.deviceService.callFeatureCommand(
                this.deviceUUID,
                this.featureIdentifier,
                name,
                this.paramValues
            )
        );
        console.log(this.returnValues);
        // console.log(this.returnValues.find(item => item.name === name.toLowerCase()).value);
    }
}
