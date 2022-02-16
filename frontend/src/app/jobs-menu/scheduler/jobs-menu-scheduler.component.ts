import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms'
import { FormBuilder } from '@angular/forms'
import {JobService, ScheduledJobService, AccountService, WorkflowEditorService} from '@app/_services';
import {JobInfo, JobInfoList, WorkflowInfo} from '@app/_models';


@Component({
  selector: 'app-jobs-menu-scheduler',
  templateUrl: './jobs-menu-scheduler.component.html',
  styleUrls: ['./jobs-menu-scheduler.component.scss']
})
export class JobsMenuSchedulerComponent implements OnInit {
    filterInput;
    newScheduledJobInput;
    selectedJob = null;
    jobs: JobInfo[];  // WorkflowInfo
    jobsShown: JobInfo[];
    lastSearchTag: string = '';
  constructor(
      private formBuilder: FormBuilder,
      private jobService: JobService,
      private scheduledJobService: ScheduledJobService,
      private accountService: AccountService
  ) {
      this.filterInput = this.formBuilder.group({
        searchTagTitle: ['', [
          // Validators.required, // Validators
          Validators.min(0),
          Validators.max(100)
        ]],
      });
      this.newScheduledJobInput = this.formBuilder.group({
          executeAt: ['', [
             Validators.required,
             Validators.pattern('[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}')
          ]],
      })
  }
  getSearchTagTitle(): string {
      return this.filterInput.get('searchTagTitle').value
  }
  getScheduledJobExecutionTime(): Date {
      return this.newScheduledJobInput.get('executeAt').value
  }
  filter(searchTag: string) {
    this.lastSearchTag = searchTag
    this.jobsShown = [];
    for (let entry in this.jobs) {
        if (this.jobs[entry].title.includes(this.lastSearchTag)) {
            this.jobsShown.push(this.jobs[entry])
        }
        }
    if (this.lastSearchTag === '') {
        const tmp = this.getJobs()
        this.jobsShown = this.jobs
    }
  }
  async selectJob(job: JobInfo) {
      this.selectedJob = job
  }
  async scheduleJob(){
      this.selectedJob.execute_at = this.getScheduledJobExecutionTime()
      await this.scheduledJobService.createUserScheduledJob(this.selectedJob)
  }
  async deleteJob(id: number) {
      await this.jobService.deleteUserJob(id)
      await this.refresh()
  }
  async getJobs() {
      this.jobs = await (
            await this.jobService.getUserJobsInfo()
        ).map((jobInfo) => {
            return jobInfo
        });
    }
  async refresh() {
      await this.getJobs()
      this.filter(this.lastSearchTag)
  }
  async ngOnInit() {
      await this.getJobs()
      this.jobsShown = this.jobs
  }
  onSubmit() {
      this.filter(this.getSearchTagTitle())
  }
}
