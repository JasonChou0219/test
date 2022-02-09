import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatabasesMenuUpdateDatabaseComponent } from './databases-menu-update-database.component';

describe('UpdateDatabaseComponent', () => {
  let component: DatabasesMenuUpdateDatabaseComponent;
  let fixture: ComponentFixture<DatabasesMenuUpdateDatabaseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DatabasesMenuUpdateDatabaseComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DatabasesMenuUpdateDatabaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
