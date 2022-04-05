import { Component, OnInit, ViewChild } from '@angular/core';
import { ProtocolInfo } from '@app/_models';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { ProtocolService } from '@app/_services';
import {
    animate,
    state,
    style,
    transition,
    trigger,
} from '@angular/animations';
import {Router} from "@angular/router";

interface RowData {
    protocolInfo: ProtocolInfo;
}

@Component({
    selector: 'app-protocols-menu-overview',
    templateUrl: './protocols-menu-overview.component.html',
    styleUrls: ['./protocols-menu-overview.component.scss'],
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
export class ProtocolsMenuOverviewComponent implements OnInit {
    dataSource: MatTableDataSource<RowData>;
    tableColumns = [
        'title',
        'uuid',
        'owner',
        'edit',
    ];
    selected: number | null = null;

    @ViewChild(MatSort) sort: MatSort;
    constructor(
        public protocolService: ProtocolService,
        private router: Router,
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

    async delete(i: number) {
        await this.protocolService.deleteProtocol(this.dataSource.data[i].protocolInfo.id);
        await this.refresh();
    }

    edit(i: number) {
        this.router.navigate(['/dashboard/protocols/' + this.dataSource.data[i].protocolInfo.id + '/update/']);
    }

    async refresh() {
        await this.getProtocols();
    }

    ngOnInit(): void {
        this.getProtocols();
    }

    expand(i: number) {
        this.selected = this.selected === i ? null : i;
    }
}
