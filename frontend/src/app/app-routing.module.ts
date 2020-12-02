import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { DeviceListComponent } from './device-list/device-list.component';
import { LogViewComponent } from './log-view/log-view.component';
import { AuthGuard } from './auth.guard';
import { SchedulerComponent } from './scheduler/scheduler.component';
import { DataHandlerComponent } from './data-handler/data-handler.component';
import { AdminAreaComponent } from './admin-area/admin-area.component';
import { UserAreaComponent } from './user-area/user-area.component';
import { ExperimentsComponent } from './experiments/experiments.component';
import { ScriptsComponent } from './scripts/scripts.component';
import { AboutComponent} from './about/about.component';

const routes: Routes = [
    {
        path: '',
        component: DeviceListComponent,
        canActivate: [AuthGuard],
    },
    { path: 'login', component: LoginComponent },
    {
        path: 'scheduler',
        component: SchedulerComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'experiments',
        component: ExperimentsComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'scripts',
        component: ScriptsComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'dataHandler',
        component: DataHandlerComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'log',
        component: LogViewComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'about',
        component: AboutComponent},
    {
        path: 'adminArea',
        component: AdminAreaComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'userArea',
        component: UserAreaComponent,
        canActivate: [AuthGuard],
    },
];

@NgModule({
    imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
    exports: [RouterModule],
})
export class AppRoutingModule {}
