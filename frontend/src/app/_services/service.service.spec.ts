import { TestBed } from '@angular/core/testing'

import { ServiceService } from './service-list.service'

describe('ServiceListService', () => {
    let service: ServiceService

    beforeEach(() => {
        TestBed.configureTestingModule({})
        service = TestBed.inject(ServiceService)
    })

    it('should be created', () => {
        expect(service).toBeTruthy()
    })
})
