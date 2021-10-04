import { Component, OnInit, ViewChild, Inject } from '@angular/core';
import { Script } from '../device.service';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
    selector: 'app-edit-script',
    templateUrl: './edit-script.component.html',
    styleUrls: ['./edit-script.component.scss'],
})
export class EditScriptComponent implements OnInit {
    constructor(
        public dialogRef: MatDialogRef<EditScriptComponent>,
        @Inject(MAT_DIALOG_DATA) public name: string
    ) {}

    ngOnInit(): void {}
    save() {}
}
