import {Component, OnInit} from '@angular/core'
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { IconService } from '@app/_services';



@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss'],
})
export class AppComponent {
    title = 'SiLA 2 Manager';
    constructor(private matIconRegistry: MatIconRegistry,
                private domSanitizer: DomSanitizer,
                private iconService: IconService
    ){
        this.matIconRegistry.addSvgIcon('compass-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('compass-outline.svg')
        );
        this.matIconRegistry.addSvgIcon('compass-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/compass-outline.svg')
        );
        this.matIconRegistry.addSvgIcon('access-point-plus',
            this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/access-point-plus.svg')
    );
        this.matIconRegistry.addSvgIcon('account-circle-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/account-circle-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('account-cog-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/account-cog-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('account-multiple-plus-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/account-multiple-plus-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('application-edit-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/application-edit-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('calendar-clock-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('./assets/icons/calendar-clock-outline.svg')
    );
    //     this.matIconRegistry.addSvgIcon(
    //  'clock_outline',
    //  this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/clock-outline.svg')
    //);
        console.log('oaeusgisuadlaiugsehglaiugliaugluiseagliuaesgailuseglaseiugaseluigasleiughsaiouu')
        this.matIconRegistry.addSvgIcon('clock_outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="24" height="24" viewBox="0 0 24 24"><path d="M12,20C16.42,20 20,16.42 20,12C20,7.58 16.42,4 12,4C7.58,4 4,7.58 4,12C4,16.42 7.58,20 12,20M12,2C17.52,2 22,6.48 22,12C22,17.52 17.52,22 12,22C6.47,22 2,17.5 2,12C2,6.48 6.48,2 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z" /></svg>')
    );
        this.matIconRegistry.addSvgIcon('cog-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/cog-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('compass-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/compass-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('credit-card-wireless-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/credit-card-wireless-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('database-cog-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/database-cog-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('database-import-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/database-import-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('database-plus-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/database-plus-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('delete-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/filter-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('format-list-bulleted',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/format-list-bulleted.svg')
    );
        this.matIconRegistry.addSvgIcon('head-cog-outline',
           this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/head-cog-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('heart-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/heart-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('information-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/information-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('map-search-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/map-search-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('sitemap-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/sitemap-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('toy-brick-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/toy-brick-outline.svg')
    );
        this.matIconRegistry.addSvgIcon('web-plus',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/web-plus.svg')
    );
        this.matIconRegistry.addSvgIcon('wrench-clock',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/wrench-clock.svg')
    );
        this.matIconRegistry.addSvgIcon('wrench-outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/icons/wrench-outline.svg')
    );
        this.iconService.registerIcons();
    }
}
