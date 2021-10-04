import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { AdminAreaComponent } from './admin-area.component';

describe('AdminAreaComponent', () => {
  let component: AdminAreaComponent;
  let fixture: ComponentFixture<AdminAreaComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ AdminAreaComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminAreaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
