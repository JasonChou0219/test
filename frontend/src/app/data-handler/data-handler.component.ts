import {Component, OnInit, ViewChild} from '@angular/core';
import {
    animate,
    state,
    style,
    transition,
    trigger,
} from '@angular/animations';
import { DatabaseService, Database} from '../database.service';
import { ActivatedRoute } from '@angular/router';
import {element} from 'protractor';
import {MatDialogRef} from '@angular/material/dialog';
import { MatTable } from '@angular/material/table';
import { MatDialog } from '@angular/material/dialog';
import {
    DeviceService,
    Device,
    DeviceStatus,
} from '../device.service';
import {DatabaseLinkComponent} from '../database-link/database-link.component';

interface RowData {
    device: Device;
    status: DeviceStatus;
    // database: Database;
    detailsLoaded: boolean;
}

@Component({
  selector: 'app-data-handler',
  templateUrl: './data-handler.component.html',
  styleUrls: ['./data-handler.component.scss'],
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
export class DataHandlerComponent implements OnInit {
    dataSource: RowData[] = [];
    dataSourceActive: RowData[] = [];
    dataSourceInactive: RowData[] = [];
    tableColumns = [
        'name',
        'database',
        'address',
        'port',
        'online',
        'status',
        'edit',
        'data_transfer',
    ];
    dataTransferCheckbox = false;
    metaDataCheckbox = false;
    selected: number | null = null;
    active: boolean | null = null;
    @ViewChild(MatTable) tableActive: MatTable<any>;
    @ViewChild(MatTable) tableInactive: MatTable<any>;

    databases = [];
    newDatabase: Database = {name: '', address: '', port: 8888, online: false, status: ''};
    database: Database;
    selectedDatabase: Database;
    addDatabase() {
        // console.log(this.databases);
        // this.database.name = this.newDatabase.name;
        // this.database.ip = this.newDatabase.ip;
        // this.database.port = this.newDatabase.port;
        const addedDatabase = this.newDatabase;
        this.databaseService.addDatabase(addedDatabase);
        window.alert(`Database ${addedDatabase.name} added`);
    }
    getDatabases() {
       this.databases = this.databaseService.getDatabases();
    }
    deleteDatabase(database) {
        // var _database: Database;
        this.selectedDatabase = this.databases.find(element => element.name === database);
        console.log(this.selectedDatabase);
        // selectedDatbase.port = ;
        // selectedDatabase.status = ;
        // selectedDatabaseonline = ;
        this.databaseService.deleteDatabase(this.selectedDatabase);
    }
  constructor(private route: ActivatedRoute,
              private databaseService: DatabaseService,
              public deviceService: DeviceService,
              public dialog: MatDialog
              ) {
        this.newDatabase = {
            name: '',
            address: '',
            port: 8888,
            status: '',
            online: false,
      };
  }
  async getDevices() {
      const deviceList = await this.deviceService.getDeviceList();
      const dataActive: RowData[] = [];
      const dataInactive: RowData[] = [];
      for (const dev of deviceList) {
          const deviceStatus = await this.deviceService.getDeviceStatus(dev.uuid);
          // if (dev.available)
          if (deviceStatus.online) {
              dataActive.push({
                  device: dev,
                  // database: this.selectedDatabase, // get the right database here!!!
                  status: {online: false, status: ''},
                  detailsLoaded: false,
              });
          }
          else {
              dataInactive.push({
                  device: dev,
                  // database: this.selectedDatabase, // get the right database here!!!
                  status: {online: false, status: ''},
                  detailsLoaded: false,
              });
          }
      }
      this.dataSourceActive = dataActive;
      this.dataSourceInactive = dataInactive;
      this.tableActive.renderRows();
      for (let i = 0; i < this.dataSourceActive.length; i++) {
          const promise = this.deviceService.getDeviceStatus(
              this.dataSourceActive[i].device.uuid
          );
          await promise.then((status) => {
              this.dataSourceActive[i].status = status;
              this.tableActive.renderRows();
          });
      }
      this.tableInactive.renderRows();
      for (let i = 0; i < this.dataSourceInactive.length; i++) {
          const promise = this.deviceService.getDeviceStatus(
              this.dataSourceInactive[i].device.uuid
          );
          await promise.then((status) => {
              this.dataSourceInactive[i].status = status;
              this.tableInactive.renderRows();
          });
      }
  }
  /*
  async getDevices() {
        const deviceList = await this.deviceService.getDeviceList();
        const data: RowData[] = [];
        for (const dev of deviceList) {
            data.push({
                device: dev,
                // database: this.selectedDatabase, // get the right database here!!!
                status: { online: false, status: '' },
                detailsLoaded: false,
            });
        }
        this.dataSource = data;
        this.table.renderRows();
        for (let i = 0; i < this.dataSource.length; i++) {
            const promise = this.deviceService.getDeviceStatus(
                this.dataSource[i].device.uuid
            );
            promise.then((status) => {
                this.dataSource[i].status = status;
                this.table.renderRows();
            });
        }
    }
    */
    async link(i: number, active: boolean) {
        if (active){
            const dialogRef = this.dialog.open(DatabaseLinkComponent, {
                data: this.dataSourceActive[i].device,
            });
            const result = await dialogRef.afterClosed().toPromise();
            await this.deviceService.setDevice(result.uuid, result);
        }
        else {
            const dialogRef = this.dialog.open(DatabaseLinkComponent, {
                data: this.dataSourceInactive[i].device,
            });
            const result = await dialogRef.afterClosed().toPromise();
            await this.deviceService.setDevice(result.uuid, result);
        }
        await this.refresh();
    }
    async refresh() {
        await this.getDevices();
    }
    showDetails(i: number, active: boolean) {
        /*const dialogRef = this.dialog.open(DeviceDetailComponent, {
            data: this.dataSource[i].device,
            width: '80%',
        });


        dialogRef.afterClosed().subscribe((result) => {});
        */
        if (active){
            this.selected = this.selected === i ? null : i;
            this.active = this.active === active ? null : active;
            this.dataSourceActive[i].detailsLoaded = true;
        }
        else {
            this.selected = this.selected === i ? null : i;
            this.active = this.active === active ? null : active;
            this.dataSourceInactive[i].detailsLoaded = true;
        }
        window.alert(`This.selected: ${this.selected}; i: ${i}; active: ${active}`);

    }
  ngOnInit(): void {
        this.databases = this.databaseService.getDatabases();
        console.log(this.databases);
        this.route.paramMap.subscribe(params => {
        // this.databases = [this.testDatabase];
        // this.selectedDatabase = this.databases.pop();
        this.getDevices();
      });
  }

}
