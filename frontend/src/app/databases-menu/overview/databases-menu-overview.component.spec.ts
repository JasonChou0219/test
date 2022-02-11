import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatabasesMenuOverviewComponent } from './databases-menu-overview.component';

describe('OverviewComponent', () => {
  let component: DatabasesMenuOverviewComponent;
  let fixture: ComponentFixture<DatabasesMenuOverviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DatabasesMenuOverviewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DatabasesMenuOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
