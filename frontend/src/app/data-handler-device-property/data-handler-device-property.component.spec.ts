import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataHandlerDevicePropertyComponent } from './data-handler-device-property.component';

describe('DataHandlerDevicePropertyComponent', () => {
  let component: DataHandlerDevicePropertyComponent;
  let fixture: ComponentFixture<DataHandlerDevicePropertyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DataHandlerDevicePropertyComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DataHandlerDevicePropertyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
