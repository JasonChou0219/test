import { Injectable } from '@angular/core'
import {
    HttpRequest,
    HttpHandler,
    HttpEvent,
    HttpInterceptor,
} from '@angular/common/http'
import { Observable } from 'rxjs'
import { User } from '@app/_models';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

    constructor() {
    }

    intercept(
        request: HttpRequest<unknown>,
        next: HttpHandler
    ): Observable<HttpEvent<unknown>> {
        const user: User = JSON.parse(localStorage.getItem('user'));
        if (user['access_token']) {
            return next.handle(
                request.clone({
                    headers: request.headers.set(
                        'Authorization',
                        'Bearer ' + user['access_token']
                    ),
                })
            )
        }
        return next.handle(request)
    }
}
