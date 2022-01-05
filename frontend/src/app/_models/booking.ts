import { Job, JobInfo } from '@app/_models'


export interface Booking {
    id?: number;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;
    execute_at: Date;
    created_at: Date;
    running: boolean;
    job: Job;
}

export interface BookingInfo {
    id?: number;
    title: string;
    description?: string;
    owner?: string;
    owner_id?: number;
    execute_at: Date;
    created_at: Date;
    running: boolean;
    job: JobInfo;
}

export interface BookingInfoList {
    data: BookingInfo[];
}

export interface BookingStatus {
    online: boolean;
    status: string;
}
