import {Component, Inject, OnInit} from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Device, DeviceService, DeviceType } from '../device.service';
import { Database, DatabaseService } from '../database.service';

@Component({
  selector: 'app-database-link',
  templateUrl: './database-link.component.html',
  styleUrls: ['./database-link.component.scss']
})

export class DatabaseLinkComponent implements OnInit {
    deviceTypes = [
        {
            value: DeviceType.SILA,
            name: this.deviceService.deviceTypeAsName(DeviceType.SILA),
        },
        {
            value: DeviceType.CUSTOM,
            name: this.deviceService.deviceTypeAsName(DeviceType.CUSTOM),
        },
        {
            value: DeviceType.SOFT,
            name: this.deviceService.deviceTypeAsName(DeviceType.SOFT),
        },
    ];
    deviceWorkCopy: Device;
    databaseWorkCopy: Database;
    databaseListWorkCopy: Database[];
  constructor(public deviceService: DeviceService,
              public databaseService: DatabaseService,
              public dialogRef: MatDialogRef<DatabaseLinkComponent>,
              @Inject(MAT_DIALOG_DATA) public device: Device,
              @Inject(MAT_DIALOG_DATA) public database: Database){
              // Try this for the databaseList!!!!@Inject(MAT_DIALOG_DATA) public database: Database) {
      /*
      this.databaseWorkCopy = {
          name: database.name,
          address: database.address,
          port: database.port,
          online: database.online,
          status: database.status,
      };
      */

      this.deviceWorkCopy = {
          // id: device.id,
          uuid: device.uuid,
          name: device.name,
          type: device.type,
          address: device.address,
          port: device.port,
          available: device.available,
          user: device.user,
          database: device.database,
      };
  }
    async getDatabases() {
        const databaseListWorkCopy = this.databaseService.getDatabaseList();
        return databaseListWorkCopy;
  }
  ngOnInit(): void {
      // this.databaseListWorkCopy = this.getDatabases();
  }

}
