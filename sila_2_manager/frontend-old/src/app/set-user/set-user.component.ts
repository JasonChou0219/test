import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { User } from '../user.service';

@Component({
    selector: 'app-set-user',
    templateUrl: './set-user.component.html',
    styleUrls: ['./set-user.component.scss'],
})
export class SetUserComponent implements OnInit {
    roles: string[] = ['user', 'admin'];
    constructor(
        public dialogRef: MatDialogRef<SetUserComponent>,
        @Inject(MAT_DIALOG_DATA) public user: User
    ) {}

    ngOnInit(): void {}
}
