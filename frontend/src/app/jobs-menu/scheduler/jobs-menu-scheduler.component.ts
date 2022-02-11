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
    this.jobsShown = [];
    for (let entry in this.jobs) {
        console.log(this.jobs[entry])
        console.log(searchTag)
        if (this.jobs[entry].title.includes(searchTag)) {
            this.jobsShown.push(this.jobs[entry])
        } else if (searchTag === '') {
            const tmp = this.getJobs()
            this.jobsShown = this.jobs
        }
    }
  }
  async selectJob(job: JobInfo) {
      this.selectedJob = job
  }
  async scheduleJob(){
      console.log('Scheduling a new job!')
      console.log(this.getScheduledJobExecutionTime())
      this.selectedJob.execute_at = this.getScheduledJobExecutionTime()
      console.log(this.selectedJob)
      // this.selectedJob
      await this.scheduledJobService.createUserScheduledJob(this.selectedJob)
  }
  async getJobs() {
      this.jobs = await (
            await this.jobService.getUserJobsInfo()
        ).map((jobInfo) => {
            return jobInfo
        });
    }
  async ngOnInit() {
      await this.getJobs()
      this.jobsShown = this.jobs
  }
  onSubmit() {
      this.filter(this.getSearchTagTitle())
  }
}
