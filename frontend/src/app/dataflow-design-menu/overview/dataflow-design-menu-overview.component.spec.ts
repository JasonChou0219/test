import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataflowDesignMenuOverviewComponent } from './dataflow-design-menu-overview.component';

describe('OverviewComponent', () => {
  let component: DataflowDesignMenuOverviewComponent;
  let fixture: ComponentFixture<DataflowDesignMenuOverviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [DataflowDesignMenuOverviewComponent]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DataflowDesignMenuOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
