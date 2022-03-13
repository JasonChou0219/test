import { Component, OnInit, ViewChild } from '@angular/core';
import { ProtocolInfo } from '@app/_models';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { ProtocolService } from '@app/_services';

interface RowData {
    protocolInfo: ProtocolInfo;
}

@Component({
    selector: 'app-protocols-menu-overview',
    templateUrl: './protocols-menu-overview.component.html',
    styleUrls: ['./protocols-menu-overview.component.scss']
})
export class ProtocolsMenuOverviewComponent implements OnInit {
    dataSource: MatTableDataSource<RowData>;
    tableColumns = [
        'title',
        'uuid',
    ];

    @ViewChild(MatSort) sort: MatSort;
    constructor(
        public protocolService: ProtocolService,
    ) {}

    async getProtocols() {
        const protocolInfoList = await this.protocolService.getProtocolInfoList();
        const data: RowData[] = [];
        for (const protocolInfo of protocolInfoList) {
            data.push({
                protocolInfo: protocolInfo,
            });
        }

        this.dataSource = new MatTableDataSource(data);
        this.dataSource.sortingDataAccessor = (item, property) => {
            switch (property) {
                case 'title': return item.protocolInfo.title;
                default: return item[property];
            }
        };
        this.dataSource.sort = this.sort;
    }

    ngOnInit(): void {
        this.getProtocols();
    }

}
