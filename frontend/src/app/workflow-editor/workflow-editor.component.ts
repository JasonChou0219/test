import { Component, OnInit } from '@angular/core';
import { ServiceService } from '@app/_services/service.service';
import { WorkflowEditorService } from '@app/_services/workflow-editor.service';
import { WorkflowInfo } from '@app/_models';
import { AddWorkflowComponent } from './add-workflow/add-workflow.component';
import { EditWorkflowComponent } from './edit-workflow/edit-workflow.component';
import { MatDialog } from '@angular/material/dialog';
import {
    animate,
    state,
    style,
    transition,
    trigger,
} from '@angular/animations';
import { FileReaderService } from '../_services/file-reader.service';
import { CodeModel } from '@ngstack/code-editor';

interface RowData {
    info: WorkflowInfo;
    model?: CodeModel;
    workflowLoaded: boolean;
}

@Component({
    selector: 'app-workflow-editor',
    templateUrl: './workflow-editor.component.html',
    styleUrls: ['./workflow-editor.component.scss'],
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
export class WorkflowEditorComponent implements OnInit {
    dataSource: RowData[];
    tableColumns = ['name', 'fileName', 'edit'];
    selected: number | null = null;
    constructor(
        private fileReaderService: FileReaderService,
        private serviceService: ServiceService,
        private workflowEditorService: WorkflowEditorService,
        public dialog: MatDialog,
    ) {}

    async createWorkflow() {
        const dialogRef = this.dialog.open(AddWorkflowComponent);
        const result = await dialogRef.afterClosed().toPromise();
        await this.workflowEditorService.createUserWorkflow({
            name: result.name,
            fileName: result.fileName,
            data: result.data,
        });
        this.getWorkflow();
    }
    async getWorkflow() {
        this.dataSource = await (
            await this.workflowEditorService.getUserWorkflowsInfo()
        ).map((workflowInfo) => {
            return { info: workflowInfo, workflowLoaded: false };
        });
    }
    async expand(i: number) {
        if (this.dataSource[i].workflowLoaded === false) {
            /*this.dataSource[i].script = await this.workflowEditorService.getUserWorkflow(
                this.dataSource[i].info.id
            );*/
            const workflow = await this.workflowEditorService.getUserWorkflow(
                this.dataSource[i].info.id
            );
            this.dataSource[i].model = {
                language: 'python',
                uri: workflow.name,
                value: workflow.data,
            };
            this.dataSource[i].workflowLoaded = true;
        }
        this.selected = this.selected === i ? null : i;
    }
    async cancel(i) {
        await this.expand(i);
        await this.getWorkflow();
            }
    refresh() {
        this.getWorkflow();
    }
    async edit(i: number) {
        const info = this.dataSource[i].info;
        const dialogRef = this.dialog.open(EditWorkflowComponent, {
            data: info.name,
        });
        const result = await dialogRef.afterClosed().toPromise();
        if (result) {
            await this.workflowEditorService.setUserWorkflowInfo({
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
        this.workflowEditorService.setUserWorkflow({
            id: info.id,
            name: info.name,
            fileName: info.fileName,
            data: model.value,
        });
    }
    async delete(i: number) {
        await this.workflowEditorService.deleteUserWorkflow(this.dataSource[i].info.id);
        this.getWorkflow();
    }

    ngOnInit(): void {
        this.getWorkflow();
    }
}
