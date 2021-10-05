import { Component, OnInit } from '@angular/core';
import { LoginService, LoginCredentials } from '../login.service';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
    hide = true;
    credentials: LoginCredentials;
    credentialsWrong = false;
    constructor(private loginService: LoginService, private router: Router) {
        this.credentials = { username: '', password: '' };
    }
    async login() {
        try {
            await this.loginService.login(this.credentials);
        } catch (error) {
            if (!(error.error instanceof ErrorEvent) && error.status === 401) {
                this.credentialsWrong = true;
            }
        }
        this.router.navigate(['/']);
    }

    ngOnInit(): void {}
}
