# Utils stuffs
import os
from threading import Thread
from time import sleep


class MiningStatusHandler(Thread):
    """
    Worker thread that print status of shared
    data every time.

    The shared data contains all informations, such as
    transactions list, if miner is ready to mine,
    if another mine has win mining game, and so on...
    """

    def __init__(self,
                 lock,
                 miningStatus,
                 canStartMiningCondition):
        """
        Constructor with parameters

        :param lock:
        """

        self.lock = lock
        self.canStartMiningCondition = canStartMiningCondition
        self.miningStatus = miningStatus

        # Init thread
        Thread.__init__(self)

    def reportMiningConfiguration(self):
        """
        Report mining configuration
        """
        os.system("clear")
        print(f"{self.miningStatus}")
        sleep(1)

    def handleMiningConfiguration(self):
        """
        Handle mining configuration.
        Conditions and NON static stuffs

        """

        # We can start mining condition
        self.miningStatus.canStartMining = len(self.miningStatus.receivedTransactions) >= self.miningStatus.miningStartThreshold
        if self.miningStatus.canStartMining:
            self.canStartMiningCondition.notifyAll()

        self.miningStatus.transactionReceivedNumber = len(self.miningStatus.receivedTransactions)

    def run(self):
        """
        Run method of thread
        """
        while True:
            with self.lock:
                self.handleMiningConfiguration()
                self.reportMiningConfiguration()
            sleep(1)
