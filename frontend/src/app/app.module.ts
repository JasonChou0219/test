import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatDialogModule } from '@angular/material/dialog';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { FormsModule } from '@angular/forms';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatIconModule } from '@angular/material/icon';
import { MatTreeModule } from '@angular/material/tree';
import { MatListModule } from '@angular/material/list';
import { MatDividerModule } from '@angular/material/divider';
import { MatRadioModule } from '@angular/material/radio';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTooltipModule } from '@angular/material/tooltip'

import { DxSchedulerModule } from 'devextreme-angular/ui/scheduler';

import { DeviceListComponent } from './device-list/device-list.component';
import { HeaderBarComponent } from './header-bar/header-bar.component';
import { DeviceDetailComponent } from './device-detail/device-detail.component';
import { AddDeviceComponent } from './add-device/add-device.component';
import { EditDeviceComponent } from './edit-device/edit-device.component';
import { LoginComponent } from './login/login.component';

import { AuthInterceptor } from './auth.interceptor';
import { HttpErrorInterceptor } from './http-error.interceptor';
import { LogViewComponent } from './log-view/log-view.component';
import { CalendarModule, DateAdapter } from 'angular-calendar';
import { adapterFactory } from 'angular-calendar/date-adapters/date-fns';
import { SchedulerComponent } from './scheduler/scheduler.component';
import { AddBookingComponent } from './add-booking/add-booking.component';
import { AdminAreaComponent } from './admin-area/admin-area.component';
import { SetUserComponent } from './set-user/set-user.component';
import { UserAreaComponent } from './user-area/user-area.component';
import { ExperimentsComponent } from './experiments/experiments.component';
import { AddExperimentComponent } from './add-experiment/add-experiment.component';
import { ScriptsComponent } from './scripts/scripts.component';
import { AddScriptComponent } from './add-script/add-script.component';
import { AboutComponent } from './about/about.component';
import { ScriptEditorComponent } from './script-editor/script-editor.component';
import { CodeEditorModule, CodeEditorService } from '@ngstack/code-editor';
import { DeviceCommandComponent } from './device-command/device-command.component';
import { DeviceFeatureComponent } from './device-feature/device-feature.component';
import { DevicePropertyComponent } from './device-property/device-property.component';
import { EditScriptComponent } from './edit-script/edit-script.component';
import { FileSelectorComponent } from './file-selector/file-selector.component';
import { EditExperimentComponent } from './edit-experiment/edit-experiment.component';
import { DataHandlerComponent } from './data-handler/data-handler.component';
import { DataHandlerDeviceDetailComponent } from './data-handler-device-detail/data-handler-device-detail.component';
import { DataHandlerDeviceCommandComponent } from './data-handler-device-command/data-handler-device-command.component';
import { DataHandlerDeviceFeatureComponent } from './data-handler-device-feature/data-handler-device-feature.component';
import { DataHandlerDevicePropertyComponent } from './data-handler-device-property/data-handler-device-property.component';
import { DatabaseLinkComponent } from './database-link/database-link.component';

@NgModule({
    declarations: [
        AppComponent,
        DeviceListComponent,
        HeaderBarComponent,
        DeviceDetailComponent,
        AddDeviceComponent,
        EditDeviceComponent,
        LoginComponent,
        LogViewComponent,
        SchedulerComponent,
        AddBookingComponent,
        DataHandlerComponent,
        AdminAreaComponent,
        SetUserComponent,
        UserAreaComponent,
        ExperimentsComponent,
        AddExperimentComponent,
        ScriptsComponent,
        AddScriptComponent,
        AboutComponent,
        ScriptEditorComponent,
        DeviceCommandComponent,
        DeviceFeatureComponent,
        DevicePropertyComponent,
        EditScriptComponent,
        FileSelectorComponent,
        EditExperimentComponent,
        DataHandlerDeviceDetailComponent,
        DataHandlerDeviceCommandComponent,
        DataHandlerDeviceFeatureComponent,
        DataHandlerDevicePropertyComponent,
        DatabaseLinkComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        BrowserAnimationsModule,
        MatTableModule,
        MatButtonModule,
        MatCardModule,
        MatToolbarModule,
        HttpClientModule,
        MatDialogModule,
        MatFormFieldModule,
        MatInputModule,
        MatSelectModule,
        FormsModule,
        MatExpansionModule,
        MatIconModule,
        MatTreeModule,
        MatListModule,
        MatDividerModule,
        MatRadioModule,
        MatCheckboxModule,
        MatDatepickerModule,
        MatSnackBarModule,
        MatTooltipModule,
        CalendarModule.forRoot({
            provide: DateAdapter,
            useFactory: adapterFactory,
        }),
        DxSchedulerModule,
        CodeEditorModule,
        CodeEditorModule.forRoot({
            baseUrl: './assets/monaco',
            typingsWorkerUrl: './assets/workers/typings-worker.js',
        }),
    ],
    providers: [
        { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
        {
            provide: HTTP_INTERCEPTORS,
            useClass: HttpErrorInterceptor,
            multi: true,
        },
    ],
    bootstrap: [AppComponent],
})
export class AppModule {}
