import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataHandlerDeviceCommandComponent } from './data-handler-device-command.component';

describe('DataHandlerDeviceCommandComponent', () => {
  let component: DataHandlerDeviceCommandComponent;
  let fixture: ComponentFixture<DataHandlerDeviceCommandComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DataHandlerDeviceCommandComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DataHandlerDeviceCommandComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
