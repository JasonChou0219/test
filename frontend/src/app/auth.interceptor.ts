import { Injectable } from '@angular/core'
import {
    HttpRequest,
    HttpHandler,
    HttpEvent,
    HttpInterceptor,
} from '@angular/common/http'
import { Observable } from 'rxjs'
import { env } from '@environments/environment';
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

        if(request.url.startsWith("./assets/")){
           return next.handle(request);
        }
        if(request.url.startsWith("${env.apiUrl}:4200/assets/")){
           return next.handle(request);
        }
        if(request.url.startsWith("${env.apiUrl}:/assets/")){
           return next.handle(request);
        }

        if(request.url.startsWith("http://localhost/api/v1/login")){
            console.log('intercepted request')
            console.log(request.url)
           return next.handle(request);
        }

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
