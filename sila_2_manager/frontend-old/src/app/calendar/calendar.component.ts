import { Component, OnInit } from '@angular/core';
import { CalendarView } from 'angular-calendar';
import { DeviceService, BookingInfo, Device } from '../device.service';
import { AddBookingComponent } from '../add-booking/add-booking.component';
import { MatDialog } from '@angular/material/dialog';
import { parse, isValid } from 'date-fns';
import { UserService } from '../user.service';

@Component({
    selector: 'app-calendar',
    templateUrl: './calendar.component.html',
    styleUrls: ['./calendar.component.scss'],
})
export class CalendarComponent implements OnInit {
    viewDate: Date = new Date();
    view: CalendarView = CalendarView.Week;
    data: any[] = [];
    deviceNames: any[] = [];
    experimentNames: any[] = [];
    userNames: any[] = [];

    constructor(
        private deviceService: DeviceService,
        private userService: UserService,
        public dialog: MatDialog
    ) {}
    refreshView() {
        //this.refresh.next();
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
        result.setMilliseconds(0);
        if (!isValid(result)) {
            result = parse(date, 'dd.MM.yyyy HH:mm', new Date());
            result.setSeconds(59);
            result.setMilliseconds(0);
            if (!isValid(result)) {
                result = parse(date, 'dd.MM.yyyy', new Date());
                result.setHours(23);
                result.setMinutes(59);
                result.setSeconds(59);
                result.setMilliseconds(0);
            }
        }
        return result;
    }
    async add() {
        const dialogRef = this.dialog.open(AddBookingComponent);
        const result = await dialogRef.afterClosed().toPromise();
        const start = this.parseFrom(result.start);
        const end = this.parseTo(result.end);
        console.log(start.getTime() / 1000);
        console.log(end.getTime() / 1000);
        await this.deviceService.bookDevice(
            result.name,
            start.getTime() / 1000,
            end.getTime() / 1000,
            1,
            result.device
        );
        await this.getBookingInfo();
        this.refreshView();
    }
    delete(event) {
        this.deviceService.deleteBooking(event.appointmentData.id as number);
    }

    async getBookingInfo() {
        this.deviceNames = (await this.deviceService.getDeviceList()).map(
            (device) => {
                return { id: device.uuid, text: device.name };
            }
        );
        this.experimentNames = (await this.deviceService.getExperiments()).map(
            (experiment) => {
                return { id: experiment.id, text: experiment.name };
            }
        );
        this.experimentNames.push({ id: -1, text: 'Unknown' });
        this.userNames = (await this.userService.getUsers()).map((user) => {
            return { id: user.id, text: user.name };
        });
        this.data = (await this.deviceService.getBookingInfo()).map(
            (bookingInfo, index) => {
                console.log(new Date(bookingInfo.start * 1000));
                console.log(new Date(bookingInfo.end * 1000));
                const experimentName = bookingInfo.experimentName
                    ? `,${bookingInfo.experimentName}`
                    : '';
                return {
                    id: bookingInfo.id,
                    startDate: new Date(bookingInfo.start * 1000),
                    endDate: new Date(bookingInfo.end * 1000),
                    text: `${bookingInfo.name} ${experimentName}`,
                    device: bookingInfo.device,
                    experiment: bookingInfo.experiment
                        ? bookingInfo.experiment
                        : -1,
                    user: bookingInfo.user,
                };
            }
        );
    }

    ngOnInit(): void {
        this.getBookingInfo();
    }
}
