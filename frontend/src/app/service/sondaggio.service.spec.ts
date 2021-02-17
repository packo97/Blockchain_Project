/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { SondaggioService } from './sondaggio.service';

describe('Service: Sondaggio', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [SondaggioService]
    });
  });

  it('should ...', inject([SondaggioService], (service: SondaggioService) => {
    expect(service).toBeTruthy();
  }));
});
