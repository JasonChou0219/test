import { Component, OnInit } from '@angular/core';
import { DatabaseInfo } from '@app/_models';
import { DatabaseService } from '@app/_services';
import { Router } from '@angular/router';

@Component({
    selector: 'app-data-acquisition-menu-add-database',
    templateUrl: './data-acquisition-menu-add-database.component.html',
    styleUrls: ['./data-acquisition-menu-add-database.component.scss']
})
export class DataAcquisitionMenuAddDatabaseComponent implements OnInit {
    databaseInfo: DatabaseInfo;

    constructor(
        public databaseService: DatabaseService,
        private router: Router
    ) {
        this.databaseInfo = {
            title: '',
            description: '',
            name: '',
            address: '',
            port: undefined,
            username: '',
            password: '',
        }
    }

    async create() {
        await this.databaseService.createDatabase(this.databaseInfo);
        this.router.navigate(['/dashboard/data-acquisition']);
    }

    cancel() {
        this.router.navigate(['/dashboard/data-acquisition']);
    }

    ngOnInit(): void {
    }

}
