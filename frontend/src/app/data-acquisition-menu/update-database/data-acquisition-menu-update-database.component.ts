import { Component, OnInit } from '@angular/core';
import { DatabaseInfo } from '@app/_models';
import { DatabaseService } from '@app/_services';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
    selector: 'app-data-acquisition-menu-update-database',
    templateUrl: './data-acquisition-menu-update-database.component.html',
    styleUrls: ['./data-acquisition-menu-update-database.component.scss']
})
export class DataAcquisitionMenuUpdateDatabaseComponent implements OnInit {
    databaseInfo: DatabaseInfo;
    id: number;

    constructor(
        public databaseService: DatabaseService,
        private router: Router,
        private route: ActivatedRoute
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

    async getDatabase() {
        await this.databaseService.getDatabase(this.id).then(
            (database) => this.databaseInfo = database,
            () => this.cancel()
        );
    }

    async update() {
        await this.databaseService.setDatabaseInfo(this.databaseInfo);
        this.router.navigate(['/dashboard/data-acquisition']);
    }

    cancel() {
        this.router.navigate(['/dashboard/data-acquisition']);
    }

    ngOnInit(): void {
        this.route.params.subscribe(params => {
            this.id = params.id;
        })
        this.getDatabase();
    }

}
