import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { env } from '@environments/environment';
import { User } from '@app/_models';

@Injectable({ providedIn: 'root' })
export class AccountService {
    private userSubject: BehaviorSubject<User>;
    public user: Observable<User>;

    constructor(
        private router: Router,
        private http: HttpClient
    ) {
        this.userSubject = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('user')));
        this.user = this.userSubject.asObservable();
    }

    public get userValue(): User {
        return this.userSubject.value;
    }

    login(username, password) {

        const body = new URLSearchParams();
        body.set('username', username);
        body.set('password', password);

        const options = {
            headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')
        };

        const result = this.http.post<User>(`${env.apiUrl}/api/v1/login/access-token`, body.toString(), options);

        return result
            .pipe(map(user => {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('user', JSON.stringify(user));
                this.userSubject.next(user);
                return user;
            }));
    }

    loggedIn(): boolean {
        const now = Math.floor(Date.now() / 1000);
        const user = localStorage.getItem('user');
        // To-do: Implement this function
        // const expirationString = localStorage.getItem('authExpiration');
        // if (expirationString == null) {
        //    return false;
        // }
        //const expiration = parseInt(expirationString, 10);
        // return expiration - now >= 0;
        return true;
    }

    isAdmin(): boolean {
        // To-do: Implement this function
        return localStorage.getItem('role') === 'admin';
    }

    logout() {
        // remove user from local storage and set current user to null
        localStorage.removeItem('user');
        this.userSubject.next(null);
        this.router.navigate(['/login']);
    }

    register(user: User) {
        return this.http.post(`${env.apiUrl}/api/v1/users/open`, user);
    }

    getAll() {
        return this.http.get<User[]>(`${env.apiUrl}/api/v1/users/`);
    }

    getById(id: string) {
        return this.http.get<User>(`${env.apiUrl}/users/${id}`);
    }

    update(id, params) {
        return this.http.put(`${env.apiUrl}/users/${id}`, params)
            .pipe(map(x => {
                // update stored user if the logged in user updated their own record
                if (id == this.userValue.id) {
                    // update local storage
                    const user = { ...this.userValue, ...params };
                    localStorage.setItem('user', JSON.stringify(user));

                    // publish updated user to subscribers
                    this.userSubject.next(user);
                }
                return x;
            }));
    }

    delete(id: string) {
        return this.http.delete(`${env.apiUrl}/users/${id}`)
            .pipe(map(x => {
                // auto logout if the logged in user deleted their own record
                if (id == this.userValue.id) {
                    this.logout();
                }
                return x;
            }));
    }
}
