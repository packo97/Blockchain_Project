# Utils stuffs
from os import system
from threading import Thread
from time import sleep


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

        # Init thread
        Thread.__init__(self)

    def reportMiningConfiguration(self):
        """
        Report mining configuration
        """
        print(f"{self.miningStatus}")
        print("\n\n")
        # system("clear")
        sleep(2)

    def handleMiningConfiguration(self):
        """
        Handle mining configuration.
        Conditions and NON static stuffs

        """

        # We can start mining condition
        self.miningStatus.canStartMining = len(self.miningStatus.receivedTransactions) >= self.miningStatus.miningStartThreshold
        self.miningStatus.transactionReceivedNumber = len(self.miningStatus.receivedTransactions)

    def run(self):
        """
        Run method of thread
        """
        while True:
            with self.lock:
                self.handleMiningConfiguration()
                self.reportMiningConfiguration()
