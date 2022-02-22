import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { WorkflowInfo } from '@app/_models';
import { FileReaderService } from '@app/_services/file-reader.service';
@Component({
    selector: 'app-add-workflow',
    templateUrl: './add-workflow.component.html',
    styleUrls: ['./add-workflow.component.scss'],
})
export class AddWorkflowComponent implements OnInit {
    file: File;
    workflow: WorkflowInfo;
    constructor(
        private reader: FileReaderService,
        public dialogRef: MatDialogRef<AddWorkflowComponent>
    ) {
        this.workflow = { title: '', fileName: '', data: '', workflow_type: 'python'};
    }

    ngOnInit(): void {}
    fileSelected(file: File) {
        this.file = file;
        this.workflow.fileName = file.name;
    }
    async add() {
        console.log(this.file)
        this.workflow.data = await this.reader.readFile(this.file);
    }
}
