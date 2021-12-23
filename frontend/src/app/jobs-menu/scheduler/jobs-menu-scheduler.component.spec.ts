import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { JobsMenuSchedulerComponent } from './jobs-menu-scheduler.component';

describe('JobsMenuSchedulerComponent', () => {
  let component: JobsMenuSchedulerComponent;
  let fixture: ComponentFixture<JobsMenuSchedulerComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ JobsMenuSchedulerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobsMenuSchedulerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
