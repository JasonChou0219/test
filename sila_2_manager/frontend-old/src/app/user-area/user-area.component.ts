import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpErrorResponse } from '@angular/common/http';
import { preHashPassword } from '../user.service';

@Component({
    selector: 'app-user-area',
    templateUrl: './user-area.component.html',
    styleUrls: ['./user-area.component.scss'],
})
export class UserAreaComponent implements OnInit {
    newPassword: string;
    newPassword2: string;
    oldPassword: string;
    constructor(
        private userService: UserService,
        private snackBar: MatSnackBar
    ) {}

    showError(message: string) {
        this.snackBar.open(message, 'Close', {
            horizontalPosition: 'center',
            verticalPosition: 'top',
            panelClass: ['error'],
        });
    }
    showSucces(message: string) {
        this.snackBar.open(message, 'Close', {
            horizontalPosition: 'center',
            verticalPosition: 'top',
            panelClass: ['success'],
        });
    }

    ngOnInit(): void {}
    async changePassword() {
        if (this.newPassword === this.newPassword2) {
            const user = await this.userService.getCurrentUser();
            this.userService.resetPassword(
                user.id,
                preHashPassword(this.newPassword),
                preHashPassword(this.oldPassword)
            );
            //this.showSucces('Passwords were changed');
        } else {
            this.showError('Passwords do not match');
        }
    }
}
