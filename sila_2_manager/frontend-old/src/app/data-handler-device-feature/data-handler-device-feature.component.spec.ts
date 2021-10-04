import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataHandlerDeviceFeatureComponent } from './data-handler-device-feature.component';

describe('DataHandlerDeviceFeatureComponent', () => {
  let component: DataHandlerDeviceFeatureComponent;
  let fixture: ComponentFixture<DataHandlerDeviceFeatureComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DataHandlerDeviceFeatureComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DataHandlerDeviceFeatureComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
