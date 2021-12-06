import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { env } from '@environments/environment';

export enum ServiceType {
    SILA = 0,
    CUSTOM,
    SOFT,
}
