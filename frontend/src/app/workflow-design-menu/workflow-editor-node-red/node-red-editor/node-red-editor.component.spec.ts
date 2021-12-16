import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { NodeRedEditorComponent } from './node-red-editor.component';

describe('NodeRedEditorComponent', () => {
    let component: NodeRedEditorComponent;
    let fixture: ComponentFixture<NodeRedEditorComponent>;

    beforeEach(waitForAsync(() => {
        TestBed.configureTestingModule({
            declarations: [NodeRedEditorComponent],
        }).compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(NodeRedEditorComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
