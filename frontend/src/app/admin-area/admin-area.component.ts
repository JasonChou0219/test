import { Component, OnInit, ViewChild, ɵɵqueryRefresh } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatTable } from '@angular/material/table';
import { User, UserService } from '../user.service';
import { SetUserComponent } from '../set-user/set-user.component';
import { preHashPassword } from '../user.service';
import { NotificationService } from '../notification.service';

function generateRandomPassword(length: number): string {
    const alphaNumericChars =
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    let str = '';
    for (let i = 0; i < length; i++) {
        str +=
            alphaNumericChars[
                Math.floor(Math.random() * alphaNumericChars.length - 1)
            ];
    }
    return str;
}

@Component({
    selector: 'app-admin-area',
    templateUrl: './admin-area.component.html',
    styleUrls: ['./admin-area.component.scss'],
})
export class AdminAreaComponent implements OnInit {
    dataSource: User[] = [];
    tableColumns = ['name', 'fullName', 'role', 'edit'];
    @ViewChild(MatTable) table: MatTable<any>;
    constructor(
        private userService: UserService,
        public dialog: MatDialog,
        private notificationService: NotificationService
    ) {}

    ngOnInit(): void {
        this.getUsers();
    }

    refresh() {
        this.table.renderRows();
    }

    async getUsers() {
        this.dataSource = await this.userService.getUsers();
        this.refresh();
    }
    async add() {
        const dialogRef = this.dialog.open(SetUserComponent, {
            data: {
                name: '',
                fullName: '',
                role: 'user',
            },
        });
        const password = generateRandomPassword(10);
        const result = await dialogRef.afterClosed().toPromise();
        result.newPassword = preHashPassword(password);
        await this.userService.addUser(result);
        this.getUsers();
        this.showPassword(result.name, password);
    }

    async edit(i: number) {
        const dialogRef = this.dialog.open(SetUserComponent, {
            data: Object.assign({}, this.dataSource[i]),
        });
        const result = await dialogRef.afterClosed().toPromise();
        await this.userService.updateUser(result);
        this.refresh();
    }
    async delete(i: number) {
        await this.userService.deleteUser(this.dataSource[i].id);
        this.dataSource.splice(i, 1);
        this.refresh();
    }
    showPassword(user: string, password: string) {
        this.notificationService.message(
            `New password for user ${user}: ${password}`
        );
    }

    async resetPassword(i: number) {
        const password = generateRandomPassword(10);
        await this.userService.resetPassword(
            this.dataSource[i].id,
            preHashPassword(password)
        );
        this.showPassword(this.dataSource[i].name, password);
    }
}
