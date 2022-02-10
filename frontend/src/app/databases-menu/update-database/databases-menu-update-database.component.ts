import { Component, OnInit } from '@angular/core';
import { DatabaseInfo } from '@app/_models';
import { DatabaseService } from '@app/_services';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
    selector: 'app-data-acquisition-menu-update-database',
    templateUrl: './databases-menu-update-database.component.html',
    styleUrls: ['./databases-menu-update-database.component.scss']
})
export class DatabasesMenuUpdateDatabaseComponent implements OnInit {
    databaseInfo: DatabaseInfo;
    id: number;
    form: FormGroup;
    submitted = false;

    constructor(
        public databaseService: DatabaseService,
        private router: Router,
        private route: ActivatedRoute,
        private formBuilder: FormBuilder,
    ) {
        this.databaseInfo = {
            title: '',
            description: '',
            name: '',
            address: '',
            port: undefined,
            retention_policy: '',
            username: '',
            password: '',
        }
    }

    async getDatabase() {
        await this.databaseService.getDatabase(this.id).then(
            (database) => this.databaseInfo = database,
            () => this.cancel()
        );

        this.f.title.setValue(this.databaseInfo.title);
        this.f.description.setValue(this.databaseInfo.description);
        this.f.name.setValue(this.databaseInfo.name);
        this.f.username.setValue(this.databaseInfo.username);
        this.f.password.setValue(this.databaseInfo.password);
        this.f.address.setValue(this.databaseInfo.address);
        this.f.port.setValue(this.databaseInfo.port);
        this.f.retention_policy.setValue(this.databaseInfo.retention_policy);
    }

    async update() {
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
        this.databaseInfo.retention_policy = this.f.retention_policy.value

        await this.databaseService.setDatabaseInfo(this.databaseInfo);
        this.router.navigate(['/dashboard/databases']);
    }

    cancel() {
        this.router.navigate(['/dashboard/databases']);
    }

    ngOnInit(): void {
        this.route.params.subscribe(params => {
            this.id = params.id;
        })
        this.getDatabase();

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
                Validators.max(65535)]],
            retention_policy: ['', Validators.required]
        });
    }

    get f() { return this.form.controls; }
}