import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing'

import { EditServiceComponent } from './edit-service.component'

describe('EditServiceComponent', () => {
    let component: EditServiceComponent
    let fixture: ComponentFixture<EditServiceComponent>

    beforeEach(waitForAsync(() => {
        TestBed.configureTestingModule({
            declarations: [EditServiceComponent],
        }).compileComponents()
    }))

    beforeEach(() => {
        fixture = TestBed.createComponent(EditServiceComponent)
        component = fixture.componentInstance
        fixture.detectChanges()
    })

    it('should create', () => {
        expect(component).toBeTruthy()
    })
})
