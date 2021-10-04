import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeviceCommandComponent } from './device-command.component';

describe('DeviceCommandComponent', () => {
    let component: DeviceCommandComponent;
    let fixture: ComponentFixture<DeviceCommandComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [DeviceCommandComponent],
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(DeviceCommandComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
