import { Component, OnInit, ViewChild } from '@angular/core';
import { AddExperimentComponent } from '../add-experiment/add-experiment.component';
import { MatDialog } from '@angular/material/dialog';
import { Experiment, DeviceService } from '../device.service';
import { format, parse, isValid } from 'date-fns';
import {
    ExperimentService,
    ExperimentStatus,
    ExperimentStatusMessage,
} from '../experiment.service';
import { Observable } from 'rxjs';

@Component({
    selector: 'app-jobs',
    templateUrl: './experiments.component.html',
    styleUrls: ['./experiments.component.scss'],
})
export class ExperimentsComponent implements OnInit {
    dataSource: Experiment[];
    tableColumns = [
        'name',
        'user',
        'start',
        'end',
        'devices',
        'script',
        'running',
        'edit',
    ];
    @ViewChild('table')
    table;
    experimentStatus$: Observable<ExperimentStatusMessage>;
    constructor(
        private deviceService: DeviceService,
        private experimentService: ExperimentService,
        public dialog: MatDialog
    ) {}
    parseFrom(date: string): Date {
        let result = parse(date, 'dd.MM.yyyy HH:mm:ss', new Date());
        result.setMilliseconds(0);
        if (!isValid(result)) {
            result = parse(date, 'dd.MM.yyyy HH:mm', new Date());
            result.setSeconds(0);
            result.setMilliseconds(0);
            if (!isValid(result)) {
                result = parse(date, 'dd.MM.yyyy', new Date());
                result.setHours(0);
                result.setMinutes(0);
                result.setSeconds(0);
                result.setMilliseconds(0);
            }
        }
        return result;
    }

    parseTo(date: string): Date {
        let result = parse(date, 'dd.MM.yyyy HH:mm:ss', new Date());
        result.setMilliseconds(0);
        if (!isValid(result)) {
            result = parse(date, 'dd.MM.yyyy HH:mm', new Date());
            result.setSeconds(59);
            result.setMilliseconds(0);
            if (!isValid(result)) {
                result = parse(date, 'dd.MM.yyyy', new Date());
                result.setHours(23);
                result.setMinutes(59);
                result.setSeconds(59);
                result.setMilliseconds(0);
            }
        }
        return result;
    }

    formatTimeStamp(timestamp: number): string {
        return format(timestamp * 1000, 'dd.MM.yyyy HH:mm:ss');
    }

    async createExperiment() {
        const dialogRef = this.dialog.open(AddExperimentComponent);
        const result = await dialogRef.afterClosed().toPromise();
        const start = this.parseFrom(result.start);
        const end = this.parseTo(result.end);
        await this.deviceService.createExperiment({
            name: result.name,
            start: start.getTime() / 1000,
            end: end.getTime() / 1000,
            devices: result.devices,
            scriptID: result.script,
        });
        await this.getExperiments();
    }
    async getExperiments() {
        this.dataSource = await this.deviceService.getExperiments();
        this.table.renderRows();
    }
    refresh() {}
    edit(i: number) {}
    async startExperiment(i: number) {
        await this.deviceService.startExperiment(this.dataSource[i].id);
    }
    async stopExperiment(i: number) {
        await this.deviceService.stopExperiment(this.dataSource[i].id);
    }
    async getExperimentStatus(i: number) {
        // await this.deviceService.getExperimentStatus();
        // Todo: Add implementation
    }
    async delete(i: number) {
        await this.deviceService.deleteExperiment(this.dataSource[i].id);
        await this.getExperiments();
    }

    ngOnInit(): void {
        //this.experimentStatus$ = this.experimentService.getExperimentStatusStream();
        this.experimentService.connect();
        this.getExperiments();
    }
}
