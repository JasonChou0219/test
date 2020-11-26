import { Component, OnInit } from '@angular/core';
import { Script, ScriptInfo, DeviceService } from '../device.service';
import { AddScriptComponent } from '../add-script/add-script.component';
import { EditScriptComponent } from '../edit-script/edit-script.component';
import { MatDialog } from '@angular/material/dialog';
import {
    animate,
    state,
    style,
    transition,
    trigger,
} from '@angular/animations';
import { FileReaderService } from '../file-reader.service';
import { CodeModel } from '@ngstack/code-editor';

interface RowData {
    info: ScriptInfo;
    model?: CodeModel;
    scriptLoaded: boolean;
}

@Component({
    selector: 'app-scripts',
    templateUrl: './scripts.component.html',
    styleUrls: ['./scripts.component.scss'],
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
export class ScriptsComponent implements OnInit {
    dataSource: RowData[];
    tableColumns = ['name', 'fileName', 'edit'];
    selected: number | null = null;
    constructor(
        private fileReaderService: FileReaderService,
        private deviceService: DeviceService,
        public dialog: MatDialog
    ) {}

    async createScript() {
        const dialogRef = this.dialog.open(AddScriptComponent);
        const result = await dialogRef.afterClosed().toPromise();
        await this.deviceService.createUserScript({
            name: result.name,
            fileName: result.fileName,
            data: result.data,
        });
    }
    async getScript() {
        this.dataSource = await (
            await this.deviceService.getUserScriptsInfo()
        ).map((scriptInfo) => {
            return { info: scriptInfo, scriptLoaded: false };
        });
    }
    async expand(i: number) {
        if (this.dataSource[i].scriptLoaded === false) {
            /*this.dataSource[i].script = await this.deviceService.getUserScript(
                this.dataSource[i].info.id
            );*/
            const script = await this.deviceService.getUserScript(
                this.dataSource[i].info.id
            );
            this.dataSource[i].model = {
                language: 'python',
                uri: script.name,
                value: script.data,
            };
            this.dataSource[i].scriptLoaded = true;
        }
        this.selected = this.selected === i ? null : i;
    }
    async cancel(i) {
        await this.expand(i);
        await this.getScript();
            }
    refresh() {}
    async edit(i: number) {
        const info = this.dataSource[i].info;
        const dialogRef = this.dialog.open(EditScriptComponent, {
            data: info.name,
        });
        const result = await dialogRef.afterClosed().toPromise();
        if (result) {
            await this.deviceService.setUserScriptInfo({
                id: info.id,
                name: result,
                fileName: info.fileName,
            });
        }
    }
    async fileSelected(file: File, i: number) {
        const data = await this.fileReaderService.readFile(file);
        this.dataSource[i].info.fileName = file.name;
        this.dataSource[i].model = {
            language: 'python',
            uri: this.dataSource[i].info.name,
            value: data,
        };
    }
    async save(i: number) {
        const info = this.dataSource[i].info;
        const model = this.dataSource[i].model;
        this.deviceService.setUserScript({
            id: info.id,
            name: info.name,
            fileName: info.fileName,
            data: model.value,
        });
    }
    async delete(i: number) {
        await this.deviceService.deleteUserScript(this.dataSource[i].info.id);
        this.getScript();
    }

    ngOnInit(): void {
        this.getScript();
    }
}
