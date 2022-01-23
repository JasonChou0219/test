import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTable } from '@angular/material/table';
import { DatabaseService } from '@app/_services';
import { Database, DatabaseStatus } from '@app/_models';

interface RowData {
    database: Database;
    status: DatabaseStatus;
}

@Component({
  selector: 'app-data-acquisition-menu-overview',
  templateUrl: './data-acquisition-menu-overview.component.html',
  styleUrls: ['./data-acquisition-menu-overview.component.scss']
})
export class DataAcquisitionMenuOverviewComponent implements OnInit {
    dataSource: RowData[] = [];
    tableColumns = [
        'title',
        'description',
        'name',
        'username',
        'password',
        'address',
        'port',
        'online',
        'status',
        'edit',
    ];

    @ViewChild(MatTable) table: MatTable<RowData>;
    constructor(
        public databaseService: DatabaseService,
    ) {}

    async getDatabases() {
        const databaseList = await this.databaseService.getDatabaseList();
        const data: RowData[] = [];
        for (const database of databaseList) {
            data.push({
                database: database,
                status: {online: false, status: ''}
            });
        }
        this.dataSource = data;
        this.table.renderRows();

        for (let i = 0; i < this.dataSource.length; i++) {
            const promise = this.databaseService.getDatabaseStatus(
                this.dataSource[i].database.id
            );
            promise.then((status) => {
                this.dataSource[i].status = status;
                this.table.renderRows();
            });
        }
    }

    async delete(i: number) {
        await this.databaseService.deleteDatabase(this.dataSource[i].database.id);
        await this.refresh();
    }

    async refresh() {
        await this.getDatabases();
    }

    ngOnInit() {
        this.getDatabases();
    }
}
