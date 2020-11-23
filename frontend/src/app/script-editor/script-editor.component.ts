import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { CodeModel } from '@ngstack/code-editor';

@Component({
    selector: 'app-script-editor',
    templateUrl: './script-editor.component.html',
    styleUrls: ['./script-editor.component.scss'],
})
export class ScriptEditorComponent implements OnInit {
    @Input() readOnly = false;
    @Input()
    set codeModel(value: CodeModel) {
        this._codeModel = value;
    }

    theme: 'vs';
    editorOptions = {
        contextmenu: true,
        minimap: {
            enabled: false,
        },
    };
    _codeModel: CodeModel = {
        language: 'python',
        uri: '',
        value: '',
    };
    constructor() {}

    onCodeChanged(value) {}

    ngOnInit(): void {}
}
