import { Component, OnInit } from '@angular/core';
import {
    DeviceService,
    LogEntry,
    LogLevel,
    LogFilter,
} from '../device.service';
import { format, parse, isValid } from 'date-fns';

/*class LogRange{
    log: LogEntry[];
    start = 0;
    length: number;
    constructor(log: LogEntry[]) {
        this.log = log;
        this.length = log.length;
    }
    setRange(start: number, length: number) {
        this.start = start;
        this.length = length;
    }
}*/

@Component({
    selector: 'app-log-view',
    templateUrl: './log-view.component.html',
    styleUrls: ['./log-view.component.scss'],
})
export class LogViewComponent implements OnInit {
    from: string;
    to: string;
    showInfo = true;
    showWarning = true;
    showCritical = true;
    showError = true;
    maxEntriesPerPage = 100;
    currentPage = 0;
    startIndex = 0;
    numEntries = 0;
    logView: LogEntry[] = [];
    log: LogEntry[] = [];

    constructor(public deviceService: DeviceService) {
        const to = new Date();
        const from = new Date(to);
        from.setMonth(to.getMonth() - 1);
        this.from = this.formatDate(from);
        this.to = this.formatDateWithTime(to);
    }

    hasTypeInfo(type: LogLevel): boolean {
        return type === LogLevel.INFO;
    }
    hasTypeWarning(type: LogLevel): boolean {
        return type === LogLevel.WARNING;
    }
    hasTypeCritical(type: LogLevel): boolean {
        return type === LogLevel.CRITICAL;
    }
    hasTypeError(type: LogLevel): boolean {
        return type === LogLevel.ERROR;
    }

    showEntry(type: LogLevel): boolean {
        if (this.hasTypeInfo(type) && this.showInfo) {
            return true;
        } else if (this.hasTypeWarning(type) && this.showWarning) {
            return true;
        } else if (this.hasTypeCritical(type) && this.showCritical) {
            return true;
        } else if (this.hasTypeError(type) && this.showError) {
            return true;
        }
        return false;
    }
    numPages(): number {
        return Math.max(1, Math.ceil(this.log.length / this.maxEntriesPerPage));
    }

    nextPage() {
        if (this.currentPage + 1 < this.numPages()) {
            this.currentPage++;
            this.updateView();
        }
    }
    previousPage() {
        if (this.currentPage - 1 >= 0) {
            this.currentPage--;
            this.updateView();
        }
    }
    updateIndices() {
        this.startIndex = this.currentPage * this.maxEntriesPerPage;
        this.numEntries = Math.min(
            this.maxEntriesPerPage,
            this.log.length - this.startIndex
        );
    }

    updateView() {
        this.updateIndices();
        this.logView = this.log.slice(
            this.startIndex,
            this.startIndex + this.numEntries
        );
    }

    resetView() {
        this.currentPage = 0;
        this.updateView();
    }

    formatDate(date: Date): string {
        return format(date, 'dd.MM.yyyy');
    }

    formatDateWithTime(date: Date): string {
        return format(date, 'dd.MM.yyyy HH:mm');
    }

    formatTimeStamp(timestamp: number): string {
        return format(timestamp * 1000, 'dd.MM.yyyy HH:mm:ss');
    }
    parseFrom(date: string): Date {
        let result = parse(date, 'dd.MM.yyyy HH:mm:ss', new Date());
        result.setMilliseconds(0);
        if (!isValid(result)) {
            result = parse(date, 'dd.MM.yyyy HH:mm', new Date());
            result.setSeconds(0);
            result.setMilliseconds(0);
            if (!isValid(result)) {
                result = parse(date, 'dd.MM.yyyy', new Date());
                result.setHours(0);
                result.setMinutes(0);
                result.setSeconds(0);
                result.setMilliseconds(0);
            }
        }
        return result;
    }

    parseTo(date: string): Date {
        let result = parse(date, 'dd.MM.yyyy HH:mm:ss', new Date());
        result.setMilliseconds(999);
        if (!isValid(result)) {
            result = parse(date, 'dd.MM.yyyy HH:mm', new Date());
            result.setSeconds(59);
            result.setMilliseconds(999);
            if (!isValid(result)) {
                result = parse(date, 'dd.MM.yyyy', new Date());
                result.setHours(23);
                result.setMinutes(59);
                result.setSeconds(59);
                result.setMilliseconds(999);
            }
        }
        return result;
    }

    async getLog() {
        const fromDate = this.parseFrom(this.from);
        const toDate = this.parseTo(this.to);
        const param = {
            from: undefined,
            to: undefined,
            excludeInfo: !this.showInfo,
            excludeWarning: !this.showWarning,
            excludeCritical: !this.showCritical,
            excludeError: !this.showError,
        };
        if (isValid(fromDate) && isValid(toDate)) {
            param.from = fromDate;
            param.to = toDate;
        }
        this.log = await this.deviceService.getDeviceLog(param);
        this.resetView();
    }

    ngOnInit() {
        this.getLog();
    }
}
