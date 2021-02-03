import { EventEmitter, Injectable, Output } from '@angular/core';
import { Sondaggio } from '../lista-sondaggi/lista-sondaggi.component';

@Injectable({
  providedIn: 'root'
})
export class SondaggioService {

  constructor() { }

  @Output() sondaggioEmitter: EventEmitter<any> = new EventEmitter();
  refreshListaSondaggi(sondaggio: Sondaggio) {
   this.sondaggioEmitter.emit(sondaggio);
  }

 getSondaggioAggiunto() {
  return this.sondaggioEmitter;
  }
}
