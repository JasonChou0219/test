import { Component, ViewChild, Input, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { MatSidenav } from '@angular/material/sidenav';
import {FormBuilder, FormGroup} from '@angular/forms';

@Component({
    selector: 'app-sidenav',
    templateUrl: './sidenav.component.html',
    styleUrls: ['./sidenav.component.scss'],
})
export class SidenavComponent implements OnInit {
      @ViewChild('sidenav') sidenav: MatSidenav;
      // isExpanded = true;
      @Input()
      isExpanded: boolean;
      showSubmenu: boolean = false;
      isShowing = false;
      showSubSubMenu: boolean = false;

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        fb: FormBuilder,
    ) {}
    mouseenter() {
        if (!this.isExpanded) {
            this.isShowing = true;
        }
    }

    mouseleave() {
        if (!this.isExpanded) {
            this.isShowing = false;
        }
    }

    ngOnInit() {
    }

    onSubmit() {
    }
}
