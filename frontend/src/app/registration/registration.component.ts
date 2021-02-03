import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';


@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})
export class RegistrationComponent implements OnInit {

  codice_fiscale: string;
  matricola: number;

  constructor(private route : Router,private messageService: MessageService) { }

  ngOnInit() {
  }

  registrati(){
    if(this.codice_fiscale!=null && this.matricola!=null)
      this.route.navigate(['home']);
    else
    this.messageService.add({key:'notifica', severity:'error', summary:'Errore!', detail:'Inserisci i campi richiesti'});
  }

}
