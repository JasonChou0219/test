import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { JobsMenuOverviewComponent } from './jobs-menu-overview.component';

describe('JobsMenuOverviewComponent', () => {
  let component: JobsMenuOverviewComponent;
  let fixture: ComponentFixture<JobsMenuOverviewComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ JobsMenuOverviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobsMenuOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
