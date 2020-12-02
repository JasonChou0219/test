import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { AddExperimentComponent } from './add-experiment.component';

describe('AddJobComponent', () => {
    let component: AddExperimentComponent;
    let fixture: ComponentFixture<AddExperimentComponent>;

    beforeEach(waitForAsync(() => {
        TestBed.configureTestingModule({
            declarations: [AddExperimentComponent],
        }).compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(AddExperimentComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
