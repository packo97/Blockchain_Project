from threading import Thread

from time import sleep

#from mining.MinerAlgorithm import ProofOfLottery
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
                 canStartStoringInLedgerCondition
                 ):
        """
        Constructor with parameters

        :param miningStatus: Shared current status of mining
        :param lock: Re entrant lock used to handle shared data
        """
        # Init variables
        self.miningStatus = miningStatus
        self.lock = lock
        self.canStartStoringInLedgerCondition = canStartStoringInLedgerCondition

        # Init thread
        Thread.__init__(self)

    # def uniqueList(self, a):
    #     b = []
    #     for i in a:
    #         if i not in b:
    #             b.append(i)
    #     return b
    def stringifyTransactionsListsHasSameEvents(self,
                                                transactionList1,
                                                transactionList2):
        transactionList1 = ProofOfLottery.deStringifyTransactionString(transactionList1)
        transactionList2 = ProofOfLottery.deStringifyTransactionString(transactionList2)

        events1 = [transaction.event for transaction in transactionList1]
        events1.sort()

        events2 = [transaction.event for transaction in transactionList2]
        events2.sort()

        return events1 == events2

    def transactionListIsAlreadyInTheGroup(self,
                                           transactionList,
                                           blockMiningObjectsGroup):

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

                # while len(allMiningNotifications) < len(self.miningStatus.minerConfiguration.getKnownHosts()):
                #     self.canStartStoringInLedgerCondition.wait()

                # If there is at least 1 mining notification

                # print("BY ME\n")
                # for t in self.miningStatus.blockMiningNotificationsMinedByMe:
                #     print(t)
                # print("OTHER\n")
                # for t in self.miningStatus.blockMiningNotifications:
                #     print(t)
                # print("\n")




                if len(allMiningNotifications) == len(self.miningStatus.minerConfiguration.getKnownHosts()) + 1:

                    # Make groups of lists of transactions
                    groups = []
                    for miningNotification1 in allMiningNotifications:
                        for miningNotification2 in allMiningNotifications:

                            if self.stringifyTransactionsListsHasSameEvents(miningNotification1.transactionsList,
                                                                            miningNotification2.transactionsList):

                                if not self.transactionListIsAlreadyInTheGroup(miningNotification1.transactionsList, groups):
                                    groups.append(miningNotification1)


                    winnerBlocks = []
                    for miningNotification1 in groups:
                        winnerBlock = miningNotification1

                        for miningNotification2 in allMiningNotifications:
                            if self.stringifyTransactionsListsHasSameEvents(winnerBlock.transactionsList, miningNotification2.transactionsList):
                                if winnerBlock.seed > miningNotification2.seed:
                                    winnerBlock = miningNotification2
                        winnerBlocks.append(winnerBlock)

                    #print(f"{winnerBlocks}\n")
                    # Store
                    if len(winnerBlocks) > 0:
                        ledgerHandler = LedgerHandler(self.miningStatus.minerConfiguration.getLedgerDatabasePath())
                        for block in winnerBlocks:
                            #print(f"{block} STORED")
                            ledgerHandler.insertBlockInLedger(block)

                        # Clean mining notifications
                        # Block mining notifications
                        self.miningStatus.blockMiningNotifications.clear()
                        #self.miningStatus.anotherMinerHaveMined = False

                        # Our block mining notifications
                        self.miningStatus.blockMiningNotificationsMinedByMe.clear()
                        #self.miningStatus.iHaveMined = False

                    # Clean winner blocks
                    winnerBlocks.clear()

            sleep(0.5)
