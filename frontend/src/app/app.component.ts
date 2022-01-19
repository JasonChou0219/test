import {Component, OnInit} from '@angular/core'
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { IconService } from '@app/_services';
import { env } from '@environments/environment';


@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss'],
    viewProviders: [MatIconRegistry]
})
export class AppComponent {
    title = 'SiLA 2 Manager';
    constructor(
                private matIconRegistry: MatIconRegistry,
                private domSanitizer: DomSanitizer,
                private iconService: IconService
    ){
    this.matIconRegistry.addSvgIconInNamespace('assets', 'compass-outline',
       this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/compass-outline.svg')
       );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'compass-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/compass-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'compass-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/compass-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'access-point-plus',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/access-point-plus.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'account-circle-outline',
       this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/account-circle-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'account-cog-outline',
       this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/account-cog-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'account-multiple-outline',
       this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/account-multiple-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'application-edit-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/application-edit-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'calendar-clock-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/calendar-clock-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'clock-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/clock-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'cog-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/cog-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'compass-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/compass-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'credit-card-wireless-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/credit-card-wireless-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'database-cog-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/database-cog-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'database-import-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/database-import-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'database-plus-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/database-plus-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'delete-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/delete-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'filter-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/filter-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'format-list-bulleted',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/format-list-bulleted.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'head-cog-outline',
       this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/head-cog-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'heart-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/heart-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'information-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/information-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'knime',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/knime.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'map-search-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/map-search-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'node-red',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/node-red.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'python',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/python.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'sitemap-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/sitemap-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'toy-brick-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/toy-brick-outline.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'web-plus',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/web-plus.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'wrench-clock',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/wrench-clock.svg')
    );
    this.matIconRegistry.addSvgIconInNamespace('assets', 'wrench-outline',
        this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/wrench-outline.svg')
    );

    // this.iconService.registerIcons();
    }
}
