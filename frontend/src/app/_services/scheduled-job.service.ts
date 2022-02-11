import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { env } from '@environments/environment';

import { ScheduledJob, ScheduledJobInfo, ScheduledJobInfoList, ScheduledJobStatus } from '@app/_models';


@Injectable({
    providedIn: 'root',
})
export class ScheduledJobService {
    // serverUrl = env.backendHttpUrl;
    serverUrl = env.apiUrl;
    constructor(private http: HttpClient) {
    }
    /*
    async getUserScheduledJobsInfo(): Promise<ScheduledJobInfo[]> {
        return this.http
            .get<ScheduledJobInfo[]>(`${env.apiUrl}/api/v1/scheduled_jobs/`)
            .pipe(map((scheduledJob) => scheduledJob))
            .toPromise();
    }
    */
    async getUserScheduledJobsInfo(): Promise<ScheduledJobInfo[]> {
        return this.http
            .get<ScheduledJobInfo[]>(`${env.apiUrl}/api/v1/scheduled_jobs/`)
            .pipe(map((scheduledJob) => (scheduledJob)))
            .toPromise();
    }
    async getUserJob(scheduledJobID: number): Promise<ScheduledJob> {
        return this.http
            .get<ScheduledJob>(`${env.apiUrl}/api/v1/scheduled_jobs/` + scheduledJobID)
            .toPromise();
    }
    async updateUserScheduledJobInfo(scheduledJobInfo: ScheduledJobInfo) {
        console.log('endpoint: ', scheduledJobInfo)
        return this.http
            .put(
                `${env.apiUrl}/api/v1/jscheduled_obs/${scheduledJobInfo.id}`,
                scheduledJobInfo
            )
            .toPromise();
    }
    async updateUserScheduledJob(scheduledJob: ScheduledJob) {
        return this.http
            .put(`${env.apiUrl}/api/v1/scheduled_jobs/${scheduledJob.id}/`, scheduledJob)
            .toPromise();
    }
    async createUserScheduledJob(scheduledJob: ScheduledJobInfo) {
        return this.http
            .post(`${env.apiUrl}/api/v1/scheduled_jobs/`, scheduledJob)
            .toPromise();
    }
    async deleteUserScheduledJob(scheduledJobID: number) {
        return this.http
            .delete(`${env.apiUrl}/api/v1/scheduled_jobs/${scheduledJobID}`)
            .toPromise();
    }
    async startScheduledJob(scheduledJobID: number) {
        return this.http
            .put(this.serverUrl + `/api/scheduled_jobs/${scheduledJobID}/status`, {
                running: true,
            })
            .toPromise();
    }
    async stopScheduledJob(scheduledJobID: number) {
        return this.http
            .put(this.serverUrl + `/api/scheduled_jobs/${scheduledJobID}/status`, {
                running: false,
            })
            .toPromise();
    }
    async getScheduledJobStatus(id: number): Promise<ScheduledJobStatus> {
        return this.http
            .get<ScheduledJobStatus>(this.serverUrl + '/api/jobStatus/' + id)
            .toPromise();
    }
}
