# Utils stuffs
from threading import Thread


class MiningStatusReporter(Thread):
    """
    Worker thread that print status of shared
    data every time.

    The shared data contains all informations, such as
    transactions list, if miner is ready to mine,
    if another mine has win mining game, and so on...
    """

    def __init__(self, lock, miningStatus):
        """
        Constructor with parameters

        :param lock:
        """

        self.lock = lock
        self.miningStatus = miningStatus

    def run(self):
        """
        Run method of thread
        """
        with self.lock:
            print(self.miningStatus)