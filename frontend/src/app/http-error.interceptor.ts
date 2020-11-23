import { Injectable } from '@angular/core';
import { NotificationService } from './notification.service';

import {
    HttpRequest,
    HttpHandler,
    HttpEvent,
    HttpInterceptor,
    HttpErrorResponse,
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable()
export class HttpErrorInterceptor implements HttpInterceptor {
    constructor(private notificationService: NotificationService) {}

    intercept(
        request: HttpRequest<unknown>,
        next: HttpHandler
    ): Observable<HttpEvent<unknown>> {
        return next.handle(request).pipe(
            catchError((err: HttpErrorResponse) => {
                let message: string;
                console.log(`Interceptor Error`, err);
                if (err.error instanceof ErrorEvent) {
                    message = `Error: ${err.error.message}`;
                } else {
                    if (err.status === 500) {
                        message = `Error 500: Internal Server Error`;
                    } else {
                        message = `Error ${err.status}: ${err.error.detail}`;
                    }
                }
                this.notificationService.message(message, 2000);
                console.log(message);
                return throwError(err);
            })
        );
    }
}
