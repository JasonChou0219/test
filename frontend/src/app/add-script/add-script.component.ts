import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { Script } from '../device.service';
import { FileReaderService } from '../file-reader.service';
@Component({
    selector: 'app-add-script',
    templateUrl: './add-script.component.html',
    styleUrls: ['./add-script.component.scss'],
})
export class AddScriptComponent implements OnInit {
    file: File;
    script: Script;
    constructor(
        private reader: FileReaderService,
        public dialogRef: MatDialogRef<AddScriptComponent>
    ) {
        this.script = { name: '', fileName: '', data: '' };
    }

    ngOnInit(): void {}
    fileSelected(file: File) {
        this.file = file;
        this.script.fileName = file.name;
    }
    async add() {
        this.script.data = await this.reader.readFile(this.file);
    }
}
