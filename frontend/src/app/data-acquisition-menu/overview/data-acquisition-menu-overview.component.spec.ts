import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataAcquisitionMenuOverviewComponent } from './data-acquisition-menu-overview.component';

describe('OverviewComponent', () => {
  let component: DataAcquisitionMenuOverviewComponent;
  let fixture: ComponentFixture<DataAcquisitionMenuOverviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DataAcquisitionMenuOverviewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DataAcquisitionMenuOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
