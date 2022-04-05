import { Component, OnInit } from '@angular/core';
import {ScheduledJobService} from '@app/_services';
import {ScheduledJobInfo, ScheduledJobStatus} from '@app/_models';


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
    scheduledJobs: ScheduledJobInfo[];
    selected: number | null = null;
    scheduledJobStatus = ScheduledJobStatus
  constructor(
      private scheduledJobService: ScheduledJobService,
  ) {}
  async getScheduledJobs() {
    this.scheduledJobs = await (
          await this.scheduledJobService.getUserScheduledJobsInfo()
      ).map((scheduledJobInfo) => {
          return scheduledJobInfo
      });
  }
  async refresh() {
        await this.getScheduledJobs()
    }
  async deleteScheduledJob(id: number) {
        await this.scheduledJobService.deleteUserScheduledJob(id)
        await this.refresh()
  }
  async ngOnInit() {
      await this.getScheduledJobs()
  }
  async logWebsocket() {

  }
}
