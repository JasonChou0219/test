import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { env } from '@environments/environment';

import { Job, JobInfo, JobInfoList, JobStatus } from '@app/_models';


@Injectable({
    providedIn: 'root',
})
export class JobService {
    // serverUrl = env.backendHttpUrl;
    serverUrl = env.apiUrl;
    constructor(private http: HttpClient) {
    }

    async getUserJobsInfo(): Promise<JobInfo[]> {
        return this.http
            .get<JobInfo[]>(`${env.apiUrl}/api/v1/jobs/`)
            .pipe(map((job) => job))
            .toPromise();
    }
    async getUserJob(jobID: number): Promise<Job> {
        return this.http
            .get<Job>(`${env.apiUrl}/api/v1/jobs/` + jobID)
            .toPromise();
    }
    async updateUserJobInfo(jobInfo: JobInfo) {
        console.log('endpoint: ', jobInfo)
        return this.http
            .put(
                `${env.apiUrl}/api/v1/jobs/${jobInfo.id}`,
                jobInfo
            )
            .toPromise();
    }
    async updateUserJob(job: Job) {
        return this.http
            .put(`${env.apiUrl}/api/v1/jobs/${job.id}/`, job)
            .toPromise();
    }
    async createUserJob(job: JobInfo) {
        return this.http
            .post(`${env.apiUrl}/api/v1/jobs/`, job)
            .toPromise();
    }
    async deleteUserJob(jobID: number) {
        return this.http
            .delete(`${env.apiUrl}/api/v1/jobs/${jobID}`)
            .toPromise();
    }
    async startScheduledJob(jobID: number) {
        return this.http
            .put(this.serverUrl + `/api/jobs/${jobID}/status`, {
                running: true,
            })
            .toPromise();
    }
    async stopScheduledJob(jobID: number) {
        return this.http
            .put(this.serverUrl + `/api/jobs/${jobID}/status`, {
                running: false,
            })
            .toPromise();
    }
    async getScheduledJobStatus(id: number): Promise<JobStatus> {
        return this.http
            .get<JobStatus>(this.serverUrl + '/api/jobStatus/' + id)
            .toPromise();
    }
}
