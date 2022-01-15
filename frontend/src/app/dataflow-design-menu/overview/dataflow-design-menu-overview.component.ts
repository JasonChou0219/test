import { Component, OnInit, ViewChild } from '@angular/core';

import { DataflowService } from '@app/_services'
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';

interface RowData {
    path: string;
    openapi_link: string;
    owner: string;
    created_on: string;
    last_edited_on: string;
}

@Component({
    selector: 'app-overview',
    templateUrl: './dataflow-design-menu-overview.component.html',
    styleUrls: ['./dataflow-design-menu-overview.component.scss'],
})
export class DataflowDesignMenuOverviewComponent implements OnInit {
    dataSource: MatTableDataSource<RowData>;
    tableColumns = [
        'path',
        'owner',
        'created_on',
        'last_edited_on',
    ];

    @ViewChild(MatSort) sort: MatSort;
    constructor(
        public dataflowService: DataflowService,
    ) {}

    async getDataflows() {
        const dataflowList = await this.dataflowService.getServiceList();
        const data: RowData[] = [];
        for (const dataflow of dataflowList) {
            data.push({
                path: dataflow.path,
                openapi_link: dataflow.openapi_link,
                owner: dataflow.owner,
                created_on: dataflow.created_on,
                last_edited_on: dataflow.last_edited_on,
            });
        }
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.sort = this.sort;
    }

    async refresh() {
        await this.getDataflows();
    }

    ngOnInit() {
        this.getDataflows();
    }
}
