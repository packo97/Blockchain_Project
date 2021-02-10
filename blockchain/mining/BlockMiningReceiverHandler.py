from threading import Thread

from time import sleep

from mining.MinerAlgorithm import ProofOfLottery


class BlockMiningReceiverHandler(Thread):
    """
    This class handle receiving victory notifications.

    For example when other miners receive victory notifications, it remove transactions
    already mined from other miners if any
    """

    def __init__(self,
                 miningStatus,
                 lock):
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

    def run(self):
        """
        See if there are any victory notifications
        """

        while True:
            with self.lock:

                # If another mined has sent victory notification
                if self.miningStatus.anotherMinerHaveMined:
                    # Reset my transaction list
                    newTransactions = []

                    for blockMiningNotification in self.miningStatus.blockMiningNotifications:
                        isBloockMiningRequestGood = ProofOfLottery.verify(seed=blockMiningNotification.seed,
                                                                          receivedTransactionsStringify=blockMiningNotification.transactions_list,
                                                                          blockHash=blockMiningNotification.block_hash,
                                                                          lotteryFunctionBlockHash=blockMiningNotification.lottery_number,
                                                                          minerAddress=blockMiningNotification.miner_address,
                                                                          hashedMinerAddress=blockMiningNotification.hashedMinerAddress)

                        # If request is good we can remove transactions mined
                        if isBloockMiningRequestGood:
                            minedByAnother = ProofOfLottery.deStringifyTransactionString(self.miningStatus.blockMiningNotifications)
                            newTransactionLists = [transaction for transaction in self.miningStatus.receivedTransactions if transaction not in minedByAnother]
                            self.miningStatus.receivedTransactions = newTransactionLists



                            # Update condition of mining
                            if len(self.miningStatus.receivedTransactions) < self.miningStatus.miningStartThreshold:
                                self.miningStatus.canStartMining = False

                    # Remove block mining notifications
                    self.miningStatus.blockMiningNotifications = []
                    self.miningStatus.anotherMinerHaveMined = False

            sleep(0.5)
