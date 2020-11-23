import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataHandlerDeviceDetailComponent } from './data-handler-device-detail.component';

describe('DataHandlerDeviceDetailComponent', () => {
  let component: DataHandlerDeviceDetailComponent;
  let fixture: ComponentFixture<DataHandlerDeviceDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DataHandlerDeviceDetailComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DataHandlerDeviceDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
