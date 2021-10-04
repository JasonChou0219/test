import { Component, OnInit, Input } from '@angular/core'
import { LoginService } from '../login.service'

@Component({
    selector: 'app-header-bar',
    templateUrl: './header-bar.component.html',
    styleUrls: ['./header-bar.component.scss'],
})
export class HeaderBarComponent implements OnInit {
    @Input() title: string

    constructor(public loginService: LoginService) {}

    ngOnInit(): void {}
}
