import {
    Component,
    OnInit,
    Input,
    OnChanges,
    SimpleChanges,
} from '@angular/core';
import {Device, DeviceCommand, DeviceService, DeviceStatus, FeatureCommandParam} from '../device.service';
import {DatabaseService, CheckboxParam} from '../database.service';

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
    @Input()
    featureId: number;
    @Input()
    uuid: string;
    paramValues: FeatureCommandParam[] = [];
    expand = false;
    checkboxes: CheckboxParam[] = [];

  constructor(private databaseService: DatabaseService) {}

  async setCheckboxCommandLevel(uuid: string, featureId: number, commandId: number, meta: boolean,
                                active: boolean, metaInterval: number, nonMetaInterval: number) {
      console.log(meta, active, metaInterval, nonMetaInterval, this.paramValues);
      // Toggle the current value
      if (meta === undefined || null) { meta = false; } else { meta = !meta; }
      if (active === undefined || null) { active = false; } else { active = !active; }

      await this.databaseService.setCheckboxCommandLevel(uuid, featureId, commandId,
            meta, active, metaInterval, nonMetaInterval, this.paramValues);
        // Maybe I need to refresh here,but hopefully the two-way binding works...
        // Maybe I should just pass the commandInterface
  }
    ngOnChanges(changes: SimpleChanges) {
        /*
        for (const param of this.command.parameters) {
            this.paramValues.push('');
        }
        */
        // Update and send changes of checkboxes to backend
        this.paramValues = this.command.parameters.map((param) => {
            return { name: param.identifier.toLowerCase() + '/' + param.type.toLowerCase(), value: '' };
        });
        console.log(this.paramValues);
    }

    ngOnInit(): void {
    }
}
