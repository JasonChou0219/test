import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({
    providedIn: 'root',
})
export class NotificationService {
    constructor(private snackBar: MatSnackBar) {}
    message(message: string, duration = 0) {
        this.snackBar.open(message, 'Close', {
            horizontalPosition: 'center',
            verticalPosition: 'top',
            duration,
        });
    }
}
