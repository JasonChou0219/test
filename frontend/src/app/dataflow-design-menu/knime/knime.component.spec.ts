import { ComponentFixture, TestBed } from '@angular/core/testing';

import { KnimeComponent } from './knime.component';

describe('KnimeComponent', () => {
    let component: KnimeComponent;
    let fixture: ComponentFixture<KnimeComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [KnimeComponent]
        })
            .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(KnimeComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
