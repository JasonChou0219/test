import { Component, OnInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { AccountService, AlertService } from '@app/_services';

@Component({
    selector: 'app-dashboard',
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit {
    @Input() title: string
    isExpanded = true;
    constructor(
        public accountService: AccountService,
        private route: ActivatedRoute,
        private router: Router,
    ) {
    }
    ngOnInit() {
    }

    onSubmit() {
    }
}
