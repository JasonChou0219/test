import { TestBed } from '@angular/core/testing'

import { DataflowService } from './dataflow.service'

describe('DataflowService', () => {
    let dataflow: DataflowService

    beforeEach(() => {
        TestBed.configureTestingModule({})
        dataflow = TestBed.inject(DataflowService)
    })

    it('should be created', () => {
        expect(dataflow).toBeTruthy()
    })
})
