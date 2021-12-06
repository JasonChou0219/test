import {
    Component,
    OnInit,
    Input,
    OnChanges,
    SimpleChanges,
} from '@angular/core';
import {
    ServiceCommand,
    ServiceService,
    FeatureCommandParam, FeatureCommandResult,
} from '../service.service';

@Component({
    selector: 'app-service-command',
    templateUrl: './service-command.component.html',
    styleUrls: ['./service-command.component.scss'],
})
export class ServiceCommandComponent implements OnInit, OnChanges {
    @Input()
    command: ServiceCommand;
    @Input()
    featureIdentifier: string;
    @Input()
    featureOriginator: string;
    @Input()
    featureCategory: string;
    @Input()
    featureVersionMajor: number;
    @Input()
    serviceUUID: string;
    paramValues: FeatureCommandParam[] = [];
    returnValues: FeatureCommandResult[] = [];
    expand = false;

    constructor(private serviceService: ServiceService) {}

    ngOnChanges(hanges: SimpleChanges) {
        /*for (const param of this.command.parameters) {
            this.paramValues.push('');
        }
        */

        this.paramValues = this.command.parameters.map((param) => {
            // return { name: param.identifier.toLowerCase() + '/' + param.type.toLowerCase(), value: '' };
            return { name: param.identifier + '/' + param.data_type, value: '' };
        });
        console.log(this.paramValues);
    }

    ngOnInit(): void {
        let param: FeatureCommandResult;
        for (let i = 0; i < this.command.responses.length; i++) {
            param = {
                name: 'test_name',
                value: '[None]',
            };
            this.returnValues.push(param);
        }
    }

    async callCommand(name: string) {
        console.log(
            this.returnValues = await this.serviceService.callFeatureCommand(
                this.serviceUUID,
                this.featureOriginator,
                this.featureCategory,
                this.featureIdentifier,
                this.featureVersionMajor,
                name,
                this.paramValues
            )
        );
        console.log(this.returnValues);
        // console.log(this.returnValues.find(item => item.name === name.toLowerCase()).value);
    }
}
