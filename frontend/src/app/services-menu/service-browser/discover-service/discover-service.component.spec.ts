import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { DiscoverServiceComponent } from './discover-service.component';

describe('AboutComponent', () => {
  let component: DiscoverServiceComponent;
  let fixture: ComponentFixture<DiscoverServiceComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ DiscoverServiceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DiscoverServiceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
