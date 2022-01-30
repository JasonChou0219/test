import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { DatabaseService } from '@app/_services';
import { Database, DatabaseStatus } from '@app/_models';
import { Router } from '@angular/router';
import { MatSort } from '@angular/material/sort';

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
    dataSource: MatTableDataSource<RowData>;
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

    @ViewChild(MatSort) sort: MatSort;
    constructor(
        public databaseService: DatabaseService,
        private router: Router,
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

        this.dataSource = new MatTableDataSource(data);
        this.dataSource.sortingDataAccessor = (item, property) => {
            switch (property) {
                case 'title': return item.database.title;
                default: return item[property];
            }
        };
        this.dataSource.sort = this.sort;

        for (let i = 0; i < this.dataSource.data.length; i++) {
            const promise = this.databaseService.getDatabaseStatus(
                this.dataSource.data[i].database.id
            );
            promise.then((status) => {
                this.dataSource.data[i].status = status;
            });
        }
    }

    async delete(i: number) {
        await this.databaseService.deleteDatabase(this.dataSource.data[i].database.id);
        await this.refresh();
    }

    edit(i: number) {
        this.router.navigate(['/dashboard/databases/' + this.dataSource.data[i].database.id + '/update/']);
    }

    async refresh() {
        await this.getDatabases();
    }

    ngOnInit() {
        this.getDatabases();
    }
}
