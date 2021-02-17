import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MenuItem } from 'primeng/api';
import { Sondaggio } from '../lista-sondaggi/lista-sondaggi.component';
import { SondaggioService } from '../service/sondaggio.service';

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css']
})
export class NavBarComponent implements OnInit {

  
  displayAggiuntaSondaggio: boolean = false;;
  nome: string;
  items: MenuItem[];

  constructor(private route: Router, private sondaggioService: SondaggioService) { }
  ngOnInit() {
      this.items = [
          {label: 'Home', icon: 'pi pi-fw pi-home'},
          {label: 'Aggiungi Sondaggio', icon: 'pi pi-fw pi-plus', command: () => this.mostraDialogAggiungiSondaggio()},
          {label: 'Log out', icon: 'pi pi-fw pi-sign-out', command: () => this.logout()}
      
        ];
  }

  mostraDialogAggiungiSondaggio(){
    this.displayAggiuntaSondaggio = true;
    console.log(this.displayAggiuntaSondaggio);
  }
  aggiungiSondaggio(){
    this.displayAggiuntaSondaggio = false;
    let sondaggio = new Sondaggio(this.nome, new Date())
    this.sondaggioService.refreshListaSondaggi(sondaggio);
  }

  logout() {
    this.route.navigate(['registration']);
  }

}
