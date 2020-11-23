import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeviceFeatureComponent } from './device-feature.component';

describe('DeviceFeatureComponent', () => {
  let component: DeviceFeatureComponent;
  let fixture: ComponentFixture<DeviceFeatureComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DeviceFeatureComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DeviceFeatureComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
