import {
    Component,
    OnInit,
    ViewChild,
    Input,
    Output,
    EventEmitter,
} from '@angular/core';

@Component({
    selector: 'app-file-selector',
    templateUrl: './file-selector.component.html',
    styleUrls: ['./file-selector.component.scss'],
})
export class FileSelectorComponent implements OnInit {
    @Input()
    name: string;
    @Output() fileSelect = new EventEmitter<File>();
    @ViewChild('hiddenInput')
    hiddenInput;
    constructor() {}

    ngOnInit(): void {}
    select() {
        this.hiddenInput.nativeElement.click();
    }
    selected() {
        const files = this.hiddenInput.nativeElement.files;
        if (files.length > 0) {
            this.fileSelect.emit(files[0]);
        }
    }
}
