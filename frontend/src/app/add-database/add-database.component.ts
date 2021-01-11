import { Component, Inject, OnInit } from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA, MatDialog} from '@angular/material/dialog';
import { Database, DatabaseService } from '../database.service';

@Component({
  selector: 'app-add-database',
  templateUrl: './add-database.component.html',
  styleUrls: ['./add-database.component.scss']
})
export class AddDatabaseComponent implements OnInit {
    databaseInfo: Database;
    constructor(
        public dialogRef: MatDialogRef<AddDatabaseComponent>,
        @Inject(MAT_DIALOG_DATA) public database: Database,
    ) {
        this.databaseInfo = {
            id: 0,
            name: 'InfluxDB',
            address: '127.0.0.1',
            port: 8086,
        };
    }
    ngOnInit(): void {
    }

}
