import { Component, OnInit } from '@angular/core';
import { DatabaseInfo } from '@app/_models';
import { DatabaseService } from '@app/_services';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
    selector: 'app-data-acquisition-menu-add-database',
    templateUrl: './databases-menu-add-database.component.html',
    styleUrls: ['./databases-menu-add-database.component.scss']
})
export class DatabasesMenuAddDatabaseComponent implements OnInit {
    databaseInfo: DatabaseInfo;
    form: FormGroup;
    submitted = false;

    constructor(
        public databaseService: DatabaseService,
        private router: Router,
        private formBuilder: FormBuilder,
    ) {
        this.databaseInfo = {
            title: '',
            description: '',
            name: '',
            address: '',
            port: undefined,
            username: '',
            password: '',
        }
    }

    async create() {
        this.submitted = true;

        // Stop here if form is invalid
        if (this.form.invalid) {
            return;
        }

        this.databaseInfo.title = this.f.title.value;
        this.databaseInfo.description = this.f.description.value;
        this.databaseInfo.name = this.f.name.value;
        this.databaseInfo.username = this.f.username.value;
        this.databaseInfo.password = this.f.password.value;
        this.databaseInfo.address = this.f.address.value;
        this.databaseInfo.port = this.f.port.value;

        await this.databaseService.createDatabase(this.databaseInfo);
        this.router.navigate(['/dashboard/data-acquisition']);
    }

    cancel() {
        this.router.navigate(['/dashboard/data-acquisition']);
    }

    ngOnInit(): void {
        this.form = this.formBuilder.group({
            title: ['', Validators.required],
            description: [''],
            name: ['', Validators.required],
            username: ['', Validators.required],
            password: ['', Validators.required],
            address: ['', Validators.required],
            port: ['', [Validators.required,
                        Validators.pattern('^[0-9]*$'),
                        Validators.min(0),
                        Validators.max(65535)]]
        });
    }

    get f() { return this.form.controls; }
}
