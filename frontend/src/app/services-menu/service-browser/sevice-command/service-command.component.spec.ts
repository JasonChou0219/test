import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ServiceCommandComponent } from './service-command.component';

describe('ServiceCommandComponent', () => {
    let component: ServiceCommandComponent;
    let fixture: ComponentFixture<ServiceCommandComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [ServiceCommandComponent],
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(ServiceCommandComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
