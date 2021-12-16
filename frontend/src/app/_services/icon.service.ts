import { Injectable } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

enum Icons {
    compass_outline = 'compass-outline',
    access_point_plus = 'access-point-plus',
    calendar_clock_outline = 'calendar-clock-outline'
}

@Injectable({
  providedIn: 'root',
})
export class IconService {
    constructor(
        private matIconRegistry: MatIconRegistry,
        private domSanitizer: DomSanitizer
    ) {
    }

    public registerIcons(): void {
        this.loadIcons(Object.values(Icons), '../assets/icons/');  // svg/icons
    }

    private loadIcons(iconKeys: string[], iconUrl: string): void {
        iconKeys.forEach(key => {
            this.matIconRegistry.addSvgIcon(key, this.domSanitizer.bypassSecurityTrustResourceUrl(`${iconUrl}/${key}.svg`));
        });
    }
}
