from mining.mining_utils.ProofOfLottery import ProofOfLottery


class MiningStatus:
    """
    Contains all useful shared data used by miner that
    must be handle by other workers,
    Such as:
        received transactions lists,
        minint status (if overcome mining threshold),
        ...
    """

    def __init__(self,
                 minerConfiguration,
                 miningStartThreshold):
        """
        Constructor with parameters

        :param minerConfiguration:
        :param miningStartThreshold: Threshold after we can start mining
        """
        # Init by us
        self.minerConfiguration = minerConfiguration
        self.miningStartThreshold = miningStartThreshold

        # Start mining condition
        self.receivedTransactions = []
        self.canStartMining = len(self.receivedTransactions) >= self.miningStartThreshold
        self.transactionReceivedNumber = len(self.receivedTransactions)

        # Block mining notifications
        self.blockMiningNotifications = []
        self.anotherMinerHaveMined = False

        # Our block mining notifications
        self.blockMiningNotificationsMinedByMe = []
        self.iHaveMined = False

    def __str__(self):
        """
        Stringify the status

        :return: String of current mining status
        """
        blockMiningNotificationsOfOtherMiners = '\n\t'.join([str(blockMinintNotification) for blockMinintNotification
                                                           in self.blockMiningNotifications])

        blockMiningNotificationsMinedByMe = '\n\t'.join([str(blockMinintNotification) for blockMinintNotification
                                                       in self.blockMiningNotificationsMinedByMe])

        receivedTransactions = ProofOfLottery.stringifyTransactionList(self.receivedTransactions).replace("|", "\n\t")

        return f"{self.minerConfiguration}\n"\
               f"RECEIVED TRANSACTIONS: \n\t{receivedTransactions}\n"\
               f"START TO MINE AFTER: {self.miningStartThreshold}\n"\
               f"CAN START MINING: {self.canStartMining}\n" \
               f"NUMBER OF TRANSACTIONS RECEIVED: {self.transactionReceivedNumber}\n" \
               f"ANOTHER MINER HAVE MINED: {self.anotherMinerHaveMined}\n" \
               f"BLOCK MINING NOTIFICATIONS OF OTHER MINERS: \n\t{blockMiningNotificationsOfOtherMiners}\n" \
               f"I HAVE MINED: {self.iHaveMined}\n" \
               f"MY BLOCK MINING NOTIFICATIONS: \n\t{blockMiningNotificationsMinedByMe}\n"
