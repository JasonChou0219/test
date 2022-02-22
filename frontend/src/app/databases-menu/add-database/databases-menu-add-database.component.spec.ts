import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatabasesMenuAddDatabaseComponent } from './databases-menu-add-database.component';

describe('AddDatabaseComponent', () => {
  let component: DatabasesMenuAddDatabaseComponent;
  let fixture: ComponentFixture<DatabasesMenuAddDatabaseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DatabasesMenuAddDatabaseComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DatabasesMenuAddDatabaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
