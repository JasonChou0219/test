import { Component, OnInit } from '@angular/core';
import { format } from 'date-fns';

import {JobService } from '@app/_services';
import { JobInfo, DatabaseInfo, WorkflowInfo, ServiceInfo, DataflowInfo } from '@app/_models';

// Import mocked data
import { mockDatabaseInfoList, mockWorkflowInfoList, mockServiceInfoList, mockDataflowInfoList } from '@app/_models';

@Component({
  selector: 'app-jobs-menu-create',
  templateUrl: './jobs-menu-create.component.html',
  styleUrls: ['./jobs-menu-create.component.scss']
})


export class JobsMenuCreateComponent implements OnInit {
    jobInfo: JobInfo;
    databases: DatabaseInfo[] = [];
    services: ServiceInfo[] = [];
    workflows: WorkflowInfo[] = [];
    dataflows: DataflowInfo[] = [];

    constructor(
        public jobService: JobService
    ) {
        const now = new Date();
        const today = now.getDate();
        console.log(now)
        const startDate = format(now, 'dd.MM.yyyy HH:mm');
        // const endDate = format(
        // new Date(now).setDate(today + 2),
        //     'dd.MM.yyyy HH:mm'
        // );
        this.jobInfo = {
            title: '',
            description: '',
            execute_at: now,
            created_at: now,
            running: false,
            workflow_id: null,
            workflow_name: '',
            workflow_type: '',
            workflow_execute_at: now,
            workflow_running: false,
            database_name: '',
        };

  }
  create() {
    console.log('Create function executed');
    console.log(this.jobInfo);
  }
  cancel() {
    console.log('Cancel function executed')
  }


  async ngOnInit() {
    this.services = mockServiceInfoList
    this.workflows = mockWorkflowInfoList
    this.dataflows = mockDataflowInfoList
    this.databases = mockDatabaseInfoList
  }

}
