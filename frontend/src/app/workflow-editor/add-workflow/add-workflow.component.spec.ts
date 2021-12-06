import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { AddScriptComponent } from './add-script.component';

describe('AddScriptComponent', () => {
  let component: AddScriptComponent;
  let fixture: ComponentFixture<AddScriptComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ AddScriptComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddScriptComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
