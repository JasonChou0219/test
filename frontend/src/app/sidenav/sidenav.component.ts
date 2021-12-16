import { Component, ViewChild, Input, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { MatSidenav } from '@angular/material/sidenav';
import {FormBuilder, FormGroup} from '@angular/forms';
import {MatIconRegistry} from '@angular/material/icon';
import {DomSanitizer} from '@angular/platform-browser';

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

      hideToggle: boolean = false;
      // isExpandedHome: boolean = false;
      showSubmenuHome: boolean = false;
      showSubSubMenuHome: boolean = false; // showSubSubMenuHome

      // isExpandedUser: boolean = false;
      showSubmenuUser: boolean = false;
      // isExpandedDiscover: boolean = false;
      showSubmenuDiscover: boolean = false;
      isShowing = false;


    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private matIconRegistry: MatIconRegistry,
        private domSanitizer: DomSanitizer,
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
