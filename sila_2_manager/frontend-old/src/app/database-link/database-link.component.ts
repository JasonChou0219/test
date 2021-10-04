import {Component, Inject, OnInit} from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Device } from '../device.service';
import { Database, DatabaseDeviceLink, DatabaseService } from '../database.service';

@Component({
  selector: 'app-database-link',
  templateUrl: './database-link.component.html',
  styleUrls: ['./database-link.component.scss']
})

export class DatabaseLinkComponent implements OnInit {
    databaseListWorkCopy: Database[] = [];
    databaseDeviceLink: DatabaseDeviceLink;
  constructor(public databaseService: DatabaseService,
              public dialogRef: MatDialogRef<DatabaseLinkComponent>,
              @Inject(MAT_DIALOG_DATA) public device: Device,
              @Inject(MAT_DIALOG_DATA) public database: Database){
      this.databaseDeviceLink = {
          deviceId: device.uuid,
          databaseId: database.id,
      };
  }
  async ngOnInit() {
      this.databaseListWorkCopy = await this.databaseService.getDatabases();
      const defaultDb: Database = {
          id: 0,
          name: '-',
          address: '-',
          port: 0,
          username: '',
          password: '',
      };
      this.databaseListWorkCopy.push(defaultDb);
      console.log(this.databaseListWorkCopy)
  }

}
