import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { first } from 'rxjs/operators';

import { AccountService, AlertService } from '@app/_services';
// import { LoginService, LoginCredentials } from '../login.service';
// import { HttpErrorResponse } from '@angular/common/http';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
    hide = true;
    form: FormGroup;
    loading = false;
    submitted = false;

    // credentials: LoginCredentials;
    // credentialsWrong = false;

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private accountService: AccountService,
        private alertService: AlertService
        // private loginService: LoginService,
    ) {
        // this.credentials = { username: '', password: '' };
    }
    /* async login() {
        try {
            await this.loginService.login(this.credentials);
        } catch (error) {
            if (!(error.error instance of ErrorEvent) && error.status === 401) {
                this.credentialsWrong = true;
            }
        }
        this.router.navigate(['/']);
    }
    */
    ngOnInit() {
        this.form = this.formBuilder.group({
            username: ['', Validators.required],
            password: ['', Validators.required]
            });
    }

    // convenience getter for easy access to form fields
    get f() { return this.form.controls; }

    onSubmit() {
        this.submitted = true;

        // reset alerts on submit
        this.alertService.clear()
        console.log('Print this')

        // stop here if form is invalid
        if (this.form.invalid) {
            console.log('Print this too')
            console.log(this.f.username.value)
            console.log(this.f.username.error)
            return;
        }
        this.loading = true,
        this.accountService.login(
            this.f.username.value,
            this.f.password.value
            )
            .pipe(first())
            .subscribe({
                next: () => {
                    // get return url from query parameters or default to home page
                    const returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
                    this.router.navigateByUrl(returnUrl);
                    },
                    error: error => {
                        this.alertService.error(error);
                        this.loading = false;
                    }
                });
    }
}
