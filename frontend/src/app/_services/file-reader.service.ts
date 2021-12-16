import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root',
})
export class FileReaderService {
    constructor() {}
    async readFile(file: File): Promise<any> {
        const fileReader = new FileReader();

        return new Promise((resolve, reject) => {
            fileReader.onload = (event) => {
                resolve(fileReader.result as string);
            };
            fileReader.onerror = (event) => {
                reject('Could not read File');
            };

            // If a file is created, file will be undefined.
            if (typeof file !== 'undefined') {
              fileReader.readAsText(file);
            }

        });
    }
}
