import { Component, OnInit } from '@angular/core';
import { MessageService } from 'primeng/api';
import { SondaggioService } from '../service/sondaggio.service';

export class Sondaggio{
  constructor(
    private nome: String,
    private scadenza: Date
  ){}
}

@Component({
  selector: 'app-lista-sondaggi',
  templateUrl: './lista-sondaggi.component.html',
  styleUrls: ['./lista-sondaggi.component.css']
})
export class ListaSondaggiComponent implements OnInit {

  lista_sondaggi: Sondaggio[] = [];

  constructor(private sondaggioService: SondaggioService, private messageService: MessageService) { }

  ngOnInit() {
    this.sondaggioService.getSondaggioAggiunto().subscribe(
      item => {
        this.lista_sondaggi.splice(0,0,item);
      }

    )
  }


  votaSondaggio(){
    this.messageService.add({key:'notifica', severity:'success', summary:'Ottimo!', detail:'Il tuo voto è stato salvato, grazie!'});
  }

}
