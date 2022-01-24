import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataAcquisitionMenuUpdateDatabaseComponent } from './data-acquisition-menu-update-database.component';

describe('UpdateDatabaseComponent', () => {
  let component: DataAcquisitionMenuUpdateDatabaseComponent;
  let fixture: ComponentFixture<DataAcquisitionMenuUpdateDatabaseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DataAcquisitionMenuUpdateDatabaseComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DataAcquisitionMenuUpdateDatabaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
