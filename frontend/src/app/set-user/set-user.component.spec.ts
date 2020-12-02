import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { SetUserComponent } from './set-user.component';

describe('SetUserComponent', () => {
  let component: SetUserComponent;
  let fixture: ComponentFixture<SetUserComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ SetUserComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SetUserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
