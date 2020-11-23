import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatabaseLinkComponent } from './database-link.component';

describe('DatabaseLinkComponent', () => {
  let component: DatabaseLinkComponent;
  let fixture: ComponentFixture<DatabaseLinkComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DatabaseLinkComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DatabaseLinkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
