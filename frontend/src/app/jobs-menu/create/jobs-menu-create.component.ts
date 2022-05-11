import { Component, OnInit } from '@angular/core';
import { format } from 'date-fns';

import {JobService, WorkflowEditorService, AccountService, DatabaseService, ProtocolService, DataflowService} from '@app/_services';
import {JobInfo, DatabaseInfo, WorkflowInfo, ServiceInfo, DataflowInfo, WorkflowInfoList, WorkflowInfoTuple, WorkflowInfoTupleList, ProtocolInfo } from '@app/_models';

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
    dataflows = [];
    protocols: ProtocolInfo[] = [];

    selectedProtocol: ProtocolInfo;
    selectedDatabase: DatabaseInfo;

    listProtocolInfoAndDatabaseInfo: [ProtocolInfo, DatabaseInfo][] = [];

    constructor(
        public jobService: JobService,
        private workflowEditorService: WorkflowEditorService,
        private accountService: AccountService,
        private databaseService: DatabaseService,
        private protocolService: ProtocolService,
        private dataflowService: DataflowService,
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
            execute_at: null,
            created_at: now,
            running: false,
            workflows: [],  // [Tuple(int, str, datetime)] --> []Tuple(workflow_id, workflow_type, workflow_execute_at)]
            database: '',  // Tuple(int, str, datetime) --> Tuple(database_id, database_type)
            list_protocol_and_database: [],
            dataflow_path: null,
            // dataflows: {data: null},  // [Tuple(int, str, datetime)] --> [Tuple(dataflow_id, dataflow_type, dataflow_execute_at)]
            // data_protocols: null  // [Tuple(int, str, datetime)] -->
            // [Tuple(data_protocol_id, data_protocol_type, data_protocol_execute_at)]
        };

  }

  getDate(): Date {
        return new Date();
  }
  create() {
        this.jobInfo.list_protocol_and_database = [];
    this.listProtocolInfoAndDatabaseInfo.forEach((protocolInfoAndDatabaseInfo) =>
        this.jobInfo.list_protocol_and_database.push([protocolInfoAndDatabaseInfo[0].id, protocolInfoAndDatabaseInfo[1].id]));
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

  async getProtocols() {
        this.protocols = await (
            await this.protocolService.getProtocolInfoList()
        ).map((protocolInfo) => {
            return protocolInfo
        });
  }

  async getDatabases() {
        this.databases = await (
            await this.databaseService.getDatabaseList()
        ).map((databaseInfo) => {
            return databaseInfo
        });
  }

  async getDataflows() {
        this.dataflows = await (
            await this.dataflowService.getDataflowList()
        ).map((dataflowInfo) => {
            return dataflowInfo
        });
  }

  async ngOnInit() {
    console.log(this.jobInfo)
    this.services = mockServiceInfoList
    await this.getProtocols();
    await this.getDatabases()
    await this.getWorkflows()
    await this.getDataflows()
  }

  addProtocolInfoAndDatabaseInfo() {
      this.listProtocolInfoAndDatabaseInfo.push([
          this.selectedProtocol, this.selectedDatabase
      ])

      this.selectedProtocol = undefined;
      this.selectedDatabase = undefined;
  }

  deleteProtocolAndDatabase(i: number) {
        this.listProtocolInfoAndDatabaseInfo.splice(i, 1);
  }
}
