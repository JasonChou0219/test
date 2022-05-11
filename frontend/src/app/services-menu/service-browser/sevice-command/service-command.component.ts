import {
    Component,
    OnInit,
    Input,
} from '@angular/core';
import {SilaCommand, SilaCommandParameter, SilaCommandResponse, SilaFunctionResponse} from '@app/_models';
import {ServiceService} from '@app/_services';

@Component({
    selector: 'app-service-command',
    templateUrl: './service-command.component.html',
    styleUrls: ['./service-command.component.scss'],
})
export class ServiceCommandComponent implements OnInit {
    @Input()
    command: SilaCommand;
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
    paramValues =  [];
    returnValues = [];
    inputJSON: string
    expand = false;
    selected = [];

    constructor(private serviceService: ServiceService) {}


    ngOnInit(): void {
        this.inputJSON = "{" + "\n"

        const last = this.command.parameters[this.command.parameters.length - 1]

        for (const parameter of this.command.parameters) {
            this.inputJSON = this.inputJSON.concat('"' + parameter.identifier + '": ')

            if (last.identifier !== parameter.identifier){
                this.inputJSON = this.inputJSON.concat(",")
            }
            this.inputJSON = this.inputJSON.concat('\n')
        }
        this.inputJSON = this.inputJSON.concat("}")

        for (const response of this.command.responses){
            this.selected.push(true)
        }
    }

    async callCommand(functionIdentifier: string) {

        this.returnValues = []
        this.inputJSON = "{" + "\n"

        const last = this.command.parameters[this.command.parameters.length - 1]
        let counter  = 0

        for (const parameter of this.command.parameters) {

            this.inputJSON = this.inputJSON.concat('"' + parameter.identifier + '": ')
            this.inputJSON = this.inputJSON.concat(this.paramValues[counter])

            if (last.identifier !== parameter.identifier){
                this.inputJSON = this.inputJSON.concat(",")
            }
            this.inputJSON = this.inputJSON.concat('\n')
            counter++
        }
        this.inputJSON = this.inputJSON.concat("}")

        const body =  JSON.parse(this.inputJSON)

        const responseIds = []

        for (let responseId = 0; responseId < this.selected.length; responseId++){
            if  (this.selected[responseId]){
                responseIds.push(this.command.responses[responseId].identifier)
            }
        }

        const result = await this.serviceService.getFeatureCommandResponse(
                this.serviceUUID,
                this.featureIdentifier,
                functionIdentifier,
                body,
                responseIds
        )

        if (this.selected.includes(true)) {
            for (let responseId = 0; responseId < this.selected.length; responseId++) {
                if (this.selected[responseId]) {
                    this.returnValues.push(result.response[this.command.responses[responseId].identifier])
                }
                else {
                    this.returnValues.push("")
                }
            }
        }
        else {
            for (const response of this.command.responses) {
                this.returnValues.push(result.response[response.identifier])
            }
        }
    }
}
