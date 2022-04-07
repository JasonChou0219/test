import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ProtocolsMenuOverviewComponent} from './protocols-menu-overview.component';

describe('ProtocolsMenuOverviewComponent', () => {
    let component: ProtocolsMenuOverviewComponent;
    let fixture: ComponentFixture<ProtocolsMenuOverviewComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [ProtocolsMenuOverviewComponent]
        })
            .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(ProtocolsMenuOverviewComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
