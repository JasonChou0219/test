import { Component, OnInit } from '@angular/core';


interface RowData {
    job: string;
    status: boolean;
    detailsLoaded: boolean;
}


@Component({
  selector: 'app-jobs-menu-overview',
  templateUrl: './jobs-menu-overview.component.html',
  styleUrls: ['./jobs-menu-overview.component.scss']
})
export class JobsMenuOverviewComponent implements OnInit {
    dataSource: RowData[] = [];
    tableColumns = [
        'name',
        'online',
        'edit',
    ];
    selected: number | null = null;

  constructor() { }

  ngOnInit(): void {
  }

}
