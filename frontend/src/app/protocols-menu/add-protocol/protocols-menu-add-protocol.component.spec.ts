import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProtocolsMenuAddProtocolComponent } from './protocols-menu-add-protocol.component';

describe('ProtocolsMenuAddProtocolComponent', () => {
    let component: ProtocolsMenuAddProtocolComponent;
    let fixture: ComponentFixture<ProtocolsMenuAddProtocolComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [ProtocolsMenuAddProtocolComponent]
        })
            .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(ProtocolsMenuAddProtocolComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
