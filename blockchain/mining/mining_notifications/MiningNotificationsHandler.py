from threading import Thread

from time import sleep

from ledger_handler.LedgerHandler import LedgerHandler
from mining.mining_utils.ProofOfLottery import ProofOfLottery


class MiningNotificationsHandler(Thread):
    """
    Handle mining notifications thread.
    It decide what transaction must be stored in ledger
    """

    def __init__(self,
                 miningStatus,
                 lock,
                 ):
        """
        Constructor with parameters

        :param miningStatus: Shared current status of mining
        :param lock: Re entrant lock used to handle shared data
        """
        # Init variables
        self.miningStatus = miningStatus
        self.lock = lock

        # Init thread
        Thread.__init__(self)

    def stringifyTransactionsListsHasSameEvents(self,
                                                transactionList1,
                                                transactionList2):
        """
        Verify if two transaction lists (expressed as string) contain
        the same events

        :param transactionList1: First transaction list
        :param transactionList2: Second transaction list

        :return: True if events are the same, False otherwise
        """

        # destringify transactions list
        transactionList1 = ProofOfLottery.deStringifyTransactionString(transactionList1)
        transactionList2 = ProofOfLottery.deStringifyTransactionString(transactionList2)

        # get events from transaction list and sort them
        events1 = [transaction.event for transaction in transactionList1]
        events1.sort()

        # get events from transaction list and sort them
        events2 = [transaction.event for transaction in transactionList2]
        events2.sort()

        return events1 == events2

    def transactionListIsAlreadyInTheGroup(self,
                                           transactionList,
                                           blockMiningObjectsGroup):
        """
        Verify if a transaction list is already contained in a group
        of block mining requests

        :param transactionList: Transaction list to check
        :param blockMiningObjectsGroup: Group of block mining requests

        :return: True if transaction list is in the group, False otherwise
        """

        alreadyInTheGroup = False

        for blockMiningObject in blockMiningObjectsGroup:
            if self.stringifyTransactionsListsHasSameEvents(transactionList, blockMiningObject.transactionsList):
                alreadyInTheGroup = True

        return alreadyInTheGroup

    def run(self):

        while True:

            with self.lock:

                # All mining notifications (made by me + made by others).
                # NOTE they are already verified
                allMiningNotifications = self.miningStatus.blockMiningNotificationsMinedByMe + \
                                         self.miningStatus.blockMiningNotifications

                # check if all notifications arrived are in the same number of my known hosts
                # (each miner including me made a mining notification)
                if len(allMiningNotifications) == len(self.miningStatus.minerConfiguration.getKnownHosts()) + 1:

                    # Make groups of lists of transactions
                    groups = []
                    for miningNotification1 in allMiningNotifications:
                        for miningNotification2 in allMiningNotifications:

                            if self.stringifyTransactionsListsHasSameEvents(miningNotification1.transactionsList,
                                                                            miningNotification2.transactionsList):

                                if not self.transactionListIsAlreadyInTheGroup(miningNotification1.transactionsList, groups):
                                    groups.append(miningNotification1)

                    # find the winner block checking the block with less seed
                    winnerBlocks = []
                    for miningNotification1 in groups:
                        winnerBlock = miningNotification1

                        for miningNotification2 in allMiningNotifications:
                            if self.stringifyTransactionsListsHasSameEvents(winnerBlock.transactionsList, miningNotification2.transactionsList):
                                if winnerBlock.seed > miningNotification2.seed:
                                    winnerBlock = miningNotification2
                        winnerBlocks.append(winnerBlock)

                    # Store the winner block in the ledger
                    if len(winnerBlocks) > 0:
                        ledgerHandler = LedgerHandler(self.miningStatus.minerConfiguration.getLedgerDatabasePath())
                        for block in winnerBlocks:
                            ledgerHandler.insertBlockInLedger(block)

                        # Block mining notifications cleaning
                        self.miningStatus.blockMiningNotifications.clear()

                        # Our block mining notifications cleaning
                        self.miningStatus.blockMiningNotificationsMinedByMe.clear()

                    # Clean winner blocks
                    winnerBlocks.clear()

            sleep(0.5)
