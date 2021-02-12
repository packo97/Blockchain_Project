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
                 canStartMiningCondition,
                 canStartStoringInLedgerCondition):
        """
        Constructor with parameters

        :param lock:
        """

        self.lock = lock
        self.canStartMiningCondition = canStartMiningCondition
        self.canStartStoringInLedgerCondition = canStartStoringInLedgerCondition
        self.miningStatus = miningStatus

        # Init thread
        Thread.__init__(self)

    def reportMiningConfiguration(self):
        """
        Report mining configuration
        """
        os.system("clear")
        print(f"{self.miningStatus}")

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

        # Arrived at least 1 block mining notifications
        self.miningStatus.anotherMinerHaveMined = len(self.miningStatus.blockMiningNotifications) > 0

        # I have mined at least 1 block
        self.miningStatus.iHaveMined = len(self.miningStatus.blockMiningNotificationsMinedByMe) > 0

        # We can start storing block
        allMiningNotifications = self.miningStatus.blockMiningNotificationsMinedByMe + \
                                 self.miningStatus.blockMiningNotifications

        if len(allMiningNotifications) >= len(self.miningStatus.minerConfiguration.getKnownHosts()):
            self.canStartStoringInLedgerCondition.notifyAll()

    def run(self):
        """
        Run method of thread
        """
        while True:
            with self.lock:
                self.handleMiningConfiguration()
                self.reportMiningConfiguration()
            sleep(0.5)
