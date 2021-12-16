import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
    selector: 'app-node-red-editor',
    templateUrl: './node-red-editor.component.html',
    styleUrls: ['./node-red-editor.component.scss'],
})
export class NodeRedEditorComponent implements OnInit {
    constructor() {}

    onCodeChanged(value) {}

    ngOnInit(): void {}
}
