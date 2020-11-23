import { Injectable, ɵLocaleDataIndex } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { SERVER_URL } from './device.service';
import { preHashPassword } from './user.service';

export interface LoginCredentials {
    username: string;
    password: string;
}
interface AuthToken {
    token_type?: string;
    access_token: string;
    refresh_token: string;
    expiration: string;
    role: string;
}

@Injectable({
    providedIn: 'root',
})
export class LoginService {
    url = SERVER_URL;
    constructor(private http: HttpClient) {}

    async login_old(credentials: LoginCredentials) {
        const result = await this.http
            .post<AuthToken>(this.url + '/api/login', credentials)
            .toPromise();
        localStorage.setItem('authToken', result.access_token);
        localStorage.setItem('authExpiration', result.expiration);
    }
    async login(credentials: LoginCredentials) {
        const form = new HttpParams()
            .set('grant_type', 'password')
            .set('username', credentials.username)
            .set('password', preHashPassword(credentials.password));
        const result = await this.http
            .post<AuthToken>(this.url + '/api/login', form)
            .toPromise();
        localStorage.setItem('role', result.role);
        localStorage.setItem('authToken', result.access_token);
        localStorage.setItem('authExpiration', result.expiration);
    }

    logout() {
        localStorage.removeItem('role');
        localStorage.removeItem('authToken');
        localStorage.removeItem('authExpiration');
    }

    loggedIn(): boolean {
        const now = Math.floor(Date.now() / 1000);
        const expirationString = localStorage.getItem('authExpiration');
        if (expirationString == null) {
            return false;
        }
        const expiration = parseInt(expirationString, 10);
        return expiration - now >= 0;
    }
    isAdmin(): boolean {
        return localStorage.getItem('role') === 'admin';
    }
}
