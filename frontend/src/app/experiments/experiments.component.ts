import { Component, OnInit, ViewChild } from '@angular/core';
import { AddExperimentComponent } from '../add-experiment/add-experiment.component';
import { EditExperimentComponent} from '../edit-experiment/edit-experiment.component';
import { MatDialog } from '@angular/material/dialog';
import { MatTable } from '@angular/material/table';
import {Experiment, DeviceService, Device, DeviceStatus} from '../device.service';
import { format, parse, isValid } from 'date-fns';
import {map, tap} from 'rxjs/operators';

import {
    ExperimentService,
    ExperimentStatus,
    ExperimentStatusMessage,
    ExperimentLogs,
} from '../experiment.service';
import { Observable } from 'rxjs';
import {
    animate,
    state,
    style,
    transition,
    trigger
} from '@angular/animations';

interface RowData {
    experiment: Experiment;
    experimentLogs: ExperimentLogs;
    detailsLoaded: boolean;
}

@Component({
    selector: 'app-jobs',
    templateUrl: './experiments.component.html',
    styleUrls: ['./experiments.component.scss'],
    animations: [
        trigger('detailExpand', [
            state('collapsed', style({ height: '0px', minHeight: '0' })),
            state('expanded', style({ height: '*' })),
            transition(
                'expanded <=> collapsed',
                animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')
            ),
        ]),
    ],
})
export class ExperimentsComponent implements OnInit {
    dataSource: RowData[] = [];
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
    selected: number | null = null;
    // @ViewChild('table')
    // table;
    @ViewChild(MatTable) table: MatTable<any>;
    experimentStatus$: Observable<ExperimentStatusMessage>;
    experimentLogs$: Observable<ExperimentLogs>;

    statusMap = [
        'waiting for execution',
        'submitted for execution',
        'running',
        'successful',
        'error',
        'stopped manually',
        'unkown',
    ];
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
        let data: RowData[] = [];
        const experimentList = await this.deviceService.getExperiments();
        for (const exp of experimentList) {
            let logs: ExperimentLogs = {
                experimentId: exp.id,
                logList: ['No log entries'],
            };
            data.push({
                experiment: exp,
                experimentLogs: logs,
                detailsLoaded: false,
            });
        }
        this.dataSource = data;
        this.table.renderRows();
    }
    refresh() {
        this.getExperiments();
        this.table.renderRows();
    }
    async edit(i: number) {
        const dialogRef = this.dialog.open(EditExperimentComponent, {
            data: this.dataSource[i].experiment,
        });
        const result = await dialogRef.afterClosed().toPromise();
        const start = this.parseFrom(result.start);
        const end = this.parseTo(result.end);
        await this.deviceService.editExperiment(
                result.id,
            {
                name: result.name,
                start: start.getTime() / 1000,
                end: end.getTime() / 1000,
                devices: result.devices,
                scriptID: result.scriptID,
            }
            );
        await this.getExperiments();
    }
    async startExperiment(i: number) {
        console.log(i);
        await this.deviceService.startExperiment(this.dataSource[i].experiment.id);
    }
    async stopExperiment(i: number) {
        await this.deviceService.stopExperiment(this.dataSource[i].experiment.id);
    }
    async getExperimentStatus(i: number) {
        // await this.deviceService.getExperimentStatus();
        // Todo: Add implementation
    }
    async delete(i: number) {
        await this.deviceService.deleteExperiment(this.dataSource[i].experiment.id);
        await this.getExperiments();
    }
    expand(i: number) {
        this.selected = this.selected === i ? null : i;
        this.dataSource[i].detailsLoaded = true;
    }
    checkId(i: number, logExperimentId: number, experimentId: number, logs: ExperimentLogs['logList']) {
        if (logExperimentId === experimentId) {
            // console.log(this.dataSource);
            this.dataSource[i].experimentLogs.logList = logs;
            return true;
        }
        else {
            return false;
        }
    }
    ngOnInit(): void {
        this.experimentStatus$ = this.experimentService
            .getExperimentStatusStream()
            .pipe(tap((msg) => console.log(msg)));

        this.experimentLogs$ = this.experimentService
            .getExperimentsLogsStream()
            .pipe(
                tap(
                    (msg) => (this.dataSource[
                        this.dataSource.findIndex(
                            (Element) => Element.experiment.id === msg.experimentId
                        )
                        ].experimentLogs))
            );
        // console.log(msg);
        // map((msg) => this.dataSource[msg.logList.findIndex((Element) => Element.experimentId ==
        // this.dataSource[this.dataSource.findIndex((Element) => Element.experiment.id)].experiment.id)]));
        // tap((msg) => console.log(msg)),
        this.getExperiments();
    }
}
