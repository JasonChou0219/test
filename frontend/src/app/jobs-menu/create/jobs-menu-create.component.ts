import { Component, OnInit } from '@angular/core';
import { format } from 'date-fns';

import {JobService, WorkflowEditorService, AccountService } from '@app/_services';
import {JobInfo, DatabaseInfo, WorkflowInfo, ServiceInfo, DataflowInfo, WorkflowInfoList, WorkflowInfoTuple, WorkflowInfoTupleList } from '@app/_models';

// Import mocked data
import { mockDatabaseInfoList, mockServiceInfoList, mockDataflowInfoList } from '@app/_models';

@Component({
  selector: 'app-jobs-menu-create',
  templateUrl: './jobs-menu-create.component.html',
  styleUrls: ['./jobs-menu-create.component.scss']
})


export class JobsMenuCreateComponent implements OnInit {
    jobInfo: JobInfo;
    databases: DatabaseInfo[] = [];
    services: ServiceInfo[] = [];
    workflows: WorkflowInfo[];  // WorkflowInfo
    dataflows: DataflowInfo[] = [];

    constructor(
        public jobService: JobService,
        private workflowEditorService: WorkflowEditorService,
        private accountService: AccountService
    ) {
        const now = new Date();
        const today = now.getDate();
        const startDate = format(now, 'dd.MM.yyyy HH:mm');
        // const endDate = format(
        // new Date(now).setDate(today + 2),
        //     'dd.MM.yyyy HH:mm'
        // );
        this.jobInfo = {
            title: '',
            description: '',
            owner: this.accountService.userValue.username,
            owner_id: parseInt(this.accountService.userValue.id, 10),
            execute_at: now,
            created_at: now,
            running: false,
            workflows: [],  // [Tuple(int, str, datetime)] --> []Tuple(workflow_id, workflow_type, workflow_execute_at)]
            database: '',  // Tuple(int, str, datetime) --> Tuple(database_id, database_type)
            // dataflows: {data: null},  // [Tuple(int, str, datetime)] --> [Tuple(dataflow_id, dataflow_type, dataflow_execute_at)]
            // data_protocols: null  // [Tuple(int, str, datetime)] -->
            // [Tuple(data_protocol_id, data_protocol_type, data_protocol_execute_at)]
        };

  }

  getDate(): Date {
        return new Date();
  }
  create() {
    const tmp = this.jobService.createUserJob(this.jobInfo)
  }
  cancel() {
      console.log('Cancel function executed')
  }
  async getWorkflows() {
        this.workflows = await (
            await this.workflowEditorService.getUserWorkflowsInfo()
        ).map((workflowInfo) => {
            return workflowInfo
        });
    }

  async ngOnInit() {
    console.log(this.jobInfo)
    this.services = mockServiceInfoList
    this.dataflows = mockDataflowInfoList
    this.databases = mockDatabaseInfoList
    await this.getWorkflows()
  }

}
