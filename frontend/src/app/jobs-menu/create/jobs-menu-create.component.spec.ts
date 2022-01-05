import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { JobsMenuCreateComponent } from './jobs-menu-create.component';

describe('JobsMenuCreateComponent', () => {
  let component: JobsMenuCreateComponent;
  let fixture: ComponentFixture<JobsMenuCreateComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ JobsMenuCreateComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JobsMenuCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
