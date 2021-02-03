import { Component, OnInit } from '@angular/core';
import { MessageService } from 'primeng/api';
import { Sondaggio } from '../lista-sondaggi/lista-sondaggi.component';
import { SondaggioService } from '../service/sondaggio.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  
  constructor(private messageService: MessageService) { }

  ngOnInit() {
  }



  

}
