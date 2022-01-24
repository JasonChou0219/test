import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SidenavComponent } from './sidenav/sidenav.component';
import { AboutComponent } from './settings-menu/about/about.component';
import { WorkflowEditorComponent } from './workflow-design-menu/workflow-editor/workflow-editor.component';
import { NodeRedEditorComponent } from './workflow-design-menu/workflow-editor-node-red/node-red-editor/node-red-editor.component';
import { ServiceListComponent } from './services-menu/service-browser/service-list/service-list.component';
import {JobsMenuCreateComponent} from './jobs-menu/create/jobs-menu-create.component';
import {JobsMenuOverviewComponent} from './jobs-menu/overview/jobs-menu-overview.component';
import {JobsMenuSchedulerComponent} from './jobs-menu/scheduler/jobs-menu-scheduler.component';
import { DataflowDesignMenuOverviewComponent } from "@app/dataflow-design-menu/overview/dataflow-design-menu-overview.component";
import { KnimeComponent} from "@app/dataflow-design-menu/knime/knime.component";
import { DataAcquisitionMenuOverviewComponent } from '@app/data-acquisition-menu/overview/data-acquisition-menu-overview.component';
import { DataAcquisitionMenuAddDatabaseComponent } from '@app/data-acquisition-menu/add-database/data-acquisition-menu-add-database.component';
import { DataAcquisitionMenuUpdateDatabaseComponent } from '@app/data-acquisition-menu/update-database/data-acquisition-menu-update-database.component';

import { AuthGuard } from './auth.guard';


const routes: Routes = [
    {
        path: '',
        component: DashboardComponent,
        // canActivate: [AuthGuard],
    },
    {
        path: 'login',
        component: LoginComponent,
        // canActivate: [AuthGuard],
    },
    {
        path: 'dashboard',
        component: DashboardComponent,
        //canActivate: [AuthGuard],
        children: [
            {
                 path: 'workflow_editor',
                 component: WorkflowEditorComponent,
                 canActivate: [AuthGuard],
            },
            {
                 path: 'workflow_editor_node_red',
                 component: NodeRedEditorComponent,
                 canActivate: [AuthGuard],
            },
            {
                path: 'services',
                component: ServiceListComponent
            },
            {
                path: 'about',
                component: AboutComponent
            },
            {
                path: 'create',
                component: JobsMenuCreateComponent
            },
            {
                path: 'overview',
                component: JobsMenuOverviewComponent
            },
            {
                path: 'scheduler',
                component: JobsMenuSchedulerComponent
            },
            {
                path: 'dataflows',
                component: DataflowDesignMenuOverviewComponent
            },
            {
                path: 'knime',
                component: KnimeComponent
            },
            {
                path: 'data-acquisition',
                component: DataAcquisitionMenuOverviewComponent
            },
            {
                path: 'databases/create',
                component: DataAcquisitionMenuAddDatabaseComponent
            },
            {
                path: 'databases/:id/update',
                component: DataAcquisitionMenuUpdateDatabaseComponent
            },

        ]
    },
    {
        path: 'about',
        component: AboutComponent
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
    {
        path: '**',
        redirectTo: '/dashboard',
        // canActivate: [AuthGuard],
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
