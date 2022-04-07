import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProtocolsMenuUpdateProtocolComponent } from './protocols-menu-update-protocol.component';

describe('ProtocolsMenuUpdateProtocolComponent', () => {
  let component: ProtocolsMenuUpdateProtocolComponent;
  let fixture: ComponentFixture<ProtocolsMenuUpdateProtocolComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProtocolsMenuUpdateProtocolComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProtocolsMenuUpdateProtocolComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
