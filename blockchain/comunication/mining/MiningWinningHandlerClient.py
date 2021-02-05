from threading import Thread
from time import sleep

class MiningWinningHandlerClient(Thread):

    def __init__(self,lock):
        # Init thread
        Thread.__init__(self)
        self.lock = lock

    def run(self):
        while True:
            with self.lock:
                print("Ho vinto")
                sleep(3)


