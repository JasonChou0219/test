import { Component, OnInit, ViewChild } from '@angular/core';

import { DataflowService } from '@app/_services'
import { MatTable } from "@angular/material/table";

interface RowData {
    path: string;
    openapi_link: string;
    created_on: string;
    last_edited_on: string;
}

@Component({
    selector: 'app-overview',
    templateUrl: './dataflow-design-menu-overview.component.html',
    styleUrls: ['./dataflow-design-menu-overview.component.scss'],
})
export class DataflowDesignMenuOverviewComponent implements OnInit {
    dataSource: RowData[] = [];
    tableColumns = [
        'path',
        'created_on',
        'last_edited_on',
    ];

    @ViewChild(MatTable) table: MatTable<any>;
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
                created_on: dataflow.created_on,
                last_edited_on: dataflow.last_edited_on,
            });
        }
        this.dataSource = data;
        this.table.renderRows();
    }

    async refresh() {
        await this.getDataflows();
    }

    ngOnInit() {
        this.getDataflows();
    }
}
