import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataAcquisitionMenuAddDatabaseComponent } from './data-acquisition-menu-add-database.component';

describe('AddDatabaseComponent', () => {
  let component: DataAcquisitionMenuAddDatabaseComponent;
  let fixture: ComponentFixture<DataAcquisitionMenuAddDatabaseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DataAcquisitionMenuAddDatabaseComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DataAcquisitionMenuAddDatabaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
