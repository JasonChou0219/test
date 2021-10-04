import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { SHA256 } from 'crypto-js';
import { environment } from '../environments/environment';

export interface User {
    id?: number;
    name: string;
    fullName: string;
    role: string;
    newPassword?: string;
    oldPassword?: string;
}

export function preHashPassword(password: string): string {
    return SHA256(password).toString();
}

const SERVER_URL = environment.backendHttpUrl;
@Injectable({
    providedIn: 'root',
})
export class UserService {
    constructor(private http: HttpClient) {}
    async getUsers(): Promise<User[]> {
        return this.http.get<User[]>(SERVER_URL + '/api/users').toPromise();
    }

    async getUser(id: number): Promise<User> {
        return this.http.get<User>(SERVER_URL + `/api/users/${id}`).toPromise();
    }

    async getCurrentUser(): Promise<User> {
        return this.http.get<User>(SERVER_URL + '/api/users/me').toPromise();
    }

    async addUser(user: User) {
        return this.http.post(SERVER_URL + '/api/users', user).toPromise();
    }
    async deleteUser(id: number) {
        return this.http.delete(SERVER_URL + `/api/users/${id}`).toPromise();
    }
    async updateUser(user: User) {
        return this.http
            .put(SERVER_URL + `/api/users/${user.id}`, user)
            .toPromise();
    }
    async resetPassword(id: number, newPassword: string, oldPassword?: string) {
        return this.http
            .put<string>(SERVER_URL + `/api/users/${id}/password`, {
                newPassword,
                oldPassword,
            })
            .toPromise();
    }
}
