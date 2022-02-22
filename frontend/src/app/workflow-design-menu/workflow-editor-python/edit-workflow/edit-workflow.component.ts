import { Component, OnInit, ViewChild, Inject } from '@angular/core';
import { Workflow } from '@app/_models';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
    selector: 'app-edit-workflow',
    templateUrl: './edit-workflow.component.html',
    styleUrls: ['./edit-workflow.component.scss'],
})
export class EditWorkflowComponent implements OnInit {
    constructor(
        public dialogRef: MatDialogRef<EditWorkflowComponent>,
        @Inject(MAT_DIALOG_DATA) public title: string
    ) {}

    ngOnInit(): void {}
    save() {}
}
