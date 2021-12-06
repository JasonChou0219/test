import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ServicePropertyComponent } from './service-property.component';

describe('ServicePropertyComponent', () => {
  let component: ServicePropertyComponent;
  let fixture: ComponentFixture<ServicePropertyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ServicePropertyComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ServicePropertyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
