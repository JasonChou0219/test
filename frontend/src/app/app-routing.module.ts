import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SidenavComponent } from './sidenav/sidenav.component';
import { AboutComponent } from './about/about.component';
import { WorkflowEditorComponent } from './workflow-editor/workflow-editor.component';
import { ServiceListComponent } from './service-browser/service-list/service-list.component';
import { AuthGuard } from './auth.guard';


const routes: Routes = [
    {
        path: '',
        component: DashboardComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'login',
        component: LoginComponent,
        canActivate: [AuthGuard],
    },
    {
        path: 'sidenav',
        component: SidenavComponent,
        //canActivate: [AuthGuard],
    },
    {
        path: 'about',
        component: AboutComponent
    },
    {
         path: 'workflow_editor',
         component: WorkflowEditorComponent,
         // canActivate: [AuthGuard],
    },
    {
         path: 'services',
         component: SidenavComponent,
         // canActivate: [AuthGuard],
        children: [
            {
                path: '',
                component: ServiceListComponent
            }
        ]
    },
    // {
    //     path: 'experiments',
    //     component: ExperimentsComponent,
    //     canActivate: [AuthGuard],
    // },
    // {
    //     path: 'dataHandler',
    //     component: DataHandlerComponent,
    //     canActivate: [AuthGuard],
    // },
    // {
    //     path: 'log',
    //     component: LogViewComponent,
    //     canActivate: [AuthGuard],
    // },
    //     path: 'adminArea',
    //     component: AdminAreaComponent,
    //     canActivate: [AuthGuard],
    // },
    // {
    //     path: 'userArea',
    //     component: UserAreaComponent,
    //     canActivate: [AuthGuard],
    // },
];

@NgModule({
    imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
    exports: [RouterModule],
})
export class AppRoutingModule {}
