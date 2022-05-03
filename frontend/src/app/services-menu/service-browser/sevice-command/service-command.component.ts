import {
    Component,
    OnInit,
    Input,
} from '@angular/core';
import {SilaCommand, SilaCommandParameter, SilaCommandResponse} from '@app/_models';

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
    paramValues: SilaCommandParameter[] = [];
    returnValues: SilaCommandResponse[] = [];
    expand = false;

    ngOnInit(): void {}
}
