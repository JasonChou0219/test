import {
    Component,
    OnInit,
    Input,
} from '@angular/core';
import {SilaCommand, SilaCommandParameter, SilaCommandResponse, SilaFunctionResponse} from '@app/_models';
import {ServiceService} from '@app/_services';
import {Observable, Subscription, throwError} from 'rxjs';
import {NotificationService} from '@app/notification.service';
import {catchError} from 'rxjs/operators';

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
    intermediateSelected = [];
    observableUrl: string;
    intermediateValues = [];
    observableRunning = false;
    subscription: Subscription

    constructor(private serviceService: ServiceService, private notificationService: NotificationService) {}


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

        for (const response of this.command.intermediate_responses){
            this.intermediateSelected.push(true)
        }
    }

    async callCommand(functionIdentifier: string) {
        const {body, responseIds} = this.convertJSON();

        if (body.faulty_parse_json) {
            return
        }

        const result = await this.serviceService.getUnobservableFeatureCommandResponse(
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

    async stopObservable(functionIdentifier: string){
        await this.serviceService.deleteObservable(functionIdentifier)
        for (let i = 0; i < this.command.intermediate_responses.length; i++){
            this.intermediateValues[i] = "canceled"
        }
        for (let i = 0; i < this.command.responses.length; i++){
            this.returnValues[i] = "canceled"
        }
        this.observableRunning = false
    }

    async startObservable(functionIdentifier: string){
        this.observableRunning = true;
        await this.serviceService.deleteObservable(functionIdentifier)

        const {body, responseIds, intermediateResponseIds} = this.convertJSON();

        if (body.faulty_parse_json) {
            return
        }

        console.log(  body, responseIds, intermediateResponseIds)

        const result = await this.serviceService.startObservable(
            this.serviceUUID,
            this.featureIdentifier,
            functionIdentifier,
            body,
            responseIds,
            intermediateResponseIds
        )

        this.subscription = this.serviceService.createSocket(functionIdentifier, result).subscribe(
            data =>  {
                const parsedResponse = JSON.parse(data as string)

                for (let i = 0; i < this.command.intermediate_responses.length; i++){
                    this.intermediateValues[i] = parsedResponse[result].intermediate_response
                        ? parsedResponse[result].intermediate_response[this.command.intermediate_responses[i].identifier] : "finished"
                }

                for (let i = 0; i < this.command.responses.length; i++) {

                    if (parsedResponse[result].response) {
                        this.returnValues[i] = parsedResponse[result].response[this.command.responses[i].identifier]
                        this.serviceService.deleteObservable(functionIdentifier)
                        this.observableRunning = false;
                }
                    else {
                    this.returnValues[i] = ""}

                }
        },
            err => console.log( 'err'),
            () => {
                this.subscription.unsubscribe()
                this.subscription = undefined
                console.log('The observable stream is complete')
            }
            )
    }

    private convertJSON() {
        this.returnValues = [];
        this.inputJSON = '{' + '\n';

        const last = this.command.parameters[this.command.parameters.length - 1];
        let counter = 0;
        let body = JSON.parse('{"faulty_parse_json": true}')

        for (const parameter of this.command.parameters) {

            this.inputJSON = this.inputJSON.concat('"' + parameter.identifier + '": ');
            this.inputJSON = this.inputJSON.concat(this.paramValues[counter]);

            if (last.identifier !== parameter.identifier) {
                this.inputJSON = this.inputJSON.concat(',');
            }
            this.inputJSON = this.inputJSON.concat('\n');
            counter++;
        }
        this.inputJSON = this.inputJSON.concat('}');

        try {
            body = JSON.parse(this.inputJSON);
        }
        catch (e) {
            this.notificationService.message("Could not parse JSON, please refer to the body preview", 2000)
        }
        const responseIds = [];
        const intermediateResponseIds = [];

        for (let responseId = 0; responseId < this.selected.length; responseId++) {
                if (this.selected[responseId]) {
                    responseIds.push(this.command.responses[responseId].identifier);
                }
            }

        for (let responseId = 0; responseId < this.intermediateSelected.length; responseId++) {
                if (this.intermediateSelected[responseId]) {
                    intermediateResponseIds.push(this.command.intermediate_responses[responseId].identifier);
                }
            }

        return {body, responseIds, intermediateResponseIds}

    }

}
