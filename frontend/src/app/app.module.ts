import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatDialogModule } from '@angular/material/dialog';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { HttpClient } from '@angular/common/http';


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
import { ClipboardModule } from '@angular/cdk/clipboard';
import { MatSidenavModule } from '@angular/material/sidenav';

// import { DeviceListComponent } from './device-list/device-list.component';
// import { HeaderBarComponent } from './header-bar/header-bar.component';
// import { DeviceDetailComponent } from './device-detail/device-detail.component';
// import { AddDeviceComponent } from './add-device/add-device.component';
// import { EditDeviceComponent } from './edit-device/edit-device.component';

import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SidenavComponent } from './sidenav/sidenav.component';

import { ServiceListComponent } from './services-menu/service-browser/service-list/service-list.component';
import { AddServiceComponent} from './services-menu/service-browser/add-service/add-service.component';
import { EditServiceComponent} from './services-menu/service-browser/edit-service/edit-service.component';


import { WorkflowEditorComponent } from './workflow-design-menu/workflow-editor/workflow-editor.component';
import { EditorComponent } from './workflow-design-menu/workflow-editor/editor/editor.component';
import { AddWorkflowComponent } from './workflow-design-menu/workflow-editor/add-workflow/add-workflow.component';
import { EditWorkflowComponent } from './workflow-design-menu/workflow-editor/edit-workflow/edit-workflow.component';
import { CodeEditorModule, CodeEditorService } from '@ngstack/code-editor';
import { FileSelectorComponent } from './file-selector/file-selector.component';

import { NodeRedEditorComponent } from './workflow-design-menu/workflow-editor-node-red/node-red-editor/node-red-editor.component';

import {JobsMenuCreateComponent} from './jobs-menu/create/jobs-menu-create.component';
import {JobsMenuOverviewComponent} from './jobs-menu/overview/jobs-menu-overview.component';
import {JobsMenuSchedulerComponent} from './jobs-menu/scheduler/jobs-menu-scheduler.component';

import { DataflowDesignMenuOverviewComponent } from './dataflow-design-menu/overview/dataflow-design-menu-overview.component';

import { AuthInterceptor } from './auth.interceptor';
import { HttpErrorInterceptor } from './http-error.interceptor';
// import { LogViewComponent } from './log-view/log-view.component';
// import { CalendarModule, DateAdapter } from 'angular-calendar';
// import { adapterFactory } from 'angular-calendar/date-adapters/date-fns';
// import { CalendarComponent } from './calendar/calendar.component';
// import { AddBookingComponent } from './add-booking/add-booking.component';
// import { AdminAreaComponent } from './admin-area/admin-area.component';
// import { SetUserComponent } from './set-user/set-user.component';
// import { UserAreaComponent } from './user-area/user-area.component';
// import { ExperimentsComponent } from './experiments/experiments.component';
// import { AddExperimentComponent } from './add-experiment/add-experiment.component';
// import { ScriptsComponent } from './scripts/scripts.component';
import { AboutComponent } from './settings-menu/about/about.component';
// import { DeviceCommandComponent } from './device-command/device-command.component';
// import { DeviceFeatureComponent } from './device-feature/device-feature.component';
// import { DevicePropertyComponent } from './device-property/device-property.component';
// import { EditExperimentComponent } from './edit-experiment/edit-experiment.component';
// import { DataHandlerComponent } from './data-handler/data-handler.component';
// import { DataHandlerDeviceDetailComponent } from './data-handler-device-detail/data-handler-device-detail.component';
// import { DataHandlerDeviceCommandComponent } from './data-handler-device-command/data-handler-device-command.component';
// import { DataHandlerDeviceFeatureComponent } from './data-handler-device-feature/data-handler-device-feature.component';
// import { DataHandlerDevicePropertyComponent } from './data-handler-device-property/data-handler-device-property.component';
// import { DatabaseLinkComponent } from './database-link/database-link.component';
// import { AddDatabaseComponent } from './add-database/add-database.component';
import { FooterBarComponent } from './footer-bar/footer-bar.component';
import { KnimeComponent } from './dataflow-design-menu/knime/knime.component';
import { MatSortModule } from '@angular/material/sort';


@NgModule({
    declarations: [
        AppComponent,
        // DeviceListComponent,
        // DeviceDetailComponent,
        // AddDeviceComponent,
        // EditDeviceComponent,
        LoginComponent,
        DashboardComponent,
        SidenavComponent,
        ServiceListComponent,
        AddServiceComponent,
        EditServiceComponent,
        // LogViewComponent,
        // CalendarComponent,
        // AddBookingComponent,
        // DataHandlerComponent,
        // AdminAreaComponent,
        // SetUserComponent,
        // UserAreaComponent,
        // ExperimentsComponent,
        // AddExperimentComponent,
        AboutComponent,
        WorkflowEditorComponent,
        EditorComponent,
        AddWorkflowComponent,
        EditWorkflowComponent,
        FileSelectorComponent,
        NodeRedEditorComponent,
        JobsMenuCreateComponent,
        JobsMenuOverviewComponent,
        JobsMenuSchedulerComponent,
        // DeviceCommandComponent,
        // DeviceFeatureComponent,
        // DevicePropertyComponent,
        // EditExperimentComponent,
        // DataHandlerDeviceDetailComponent,
        // DataHandlerDeviceCommandComponent,
        // DataHandlerDeviceFeatureComponent,
        // DataHandlerDevicePropertyComponent,
        // DatabaseLinkComponent,
        // AddDatabaseComponent,
        FooterBarComponent,
        DataflowDesignMenuOverviewComponent,
        KnimeComponent,
    ],
    imports: [
        BrowserModule,
        ReactiveFormsModule,
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
        MatIconModule,
        FormsModule,
        MatExpansionModule,
        MatTreeModule,
        MatListModule,
        MatDividerModule,
        MatRadioModule,
        MatCheckboxModule,
        MatDatepickerModule,
        MatSnackBarModule,
        MatTooltipModule,
        ClipboardModule,
        MatSidenavModule,
        // CalendarModule.forRoot({
        //     provide: DateAdapter,
        //     useFactory: adapterFactory,
        // }),
        CodeEditorModule,
        CodeEditorModule.forRoot({
            baseUrl: './assets/monaco',
            typingsWorkerUrl: './assets/workers/typings-worker.js',
        }),
        MatSortModule,
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
