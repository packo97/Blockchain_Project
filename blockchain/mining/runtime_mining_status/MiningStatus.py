from mining.MinerAlgorithm import ProofOfLottery


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
                 receivedTransactions,
                 miningStartThreshold):
        # Init by us
        self.minerConfiguration = minerConfiguration
        self.receivedTransactions = receivedTransactions
        self.miningStartThreshold = miningStartThreshold

        # Init by conditions / external events
        self.canStartMining = len(self.receivedTransactions) >= self.miningStartThreshold
        self.transactionReceivedNumber = len(self.receivedTransactions)

    def __str__(self):

        return f"{self.minerConfiguration}\n"\
               f"RECEIVED TRANSACTIONS: \n{ProofOfLottery.stringifyTransactionList(self.receivedTransactions)}\n"\
               f"START TO MINE AFTER: {self.miningStartThreshold}\n"\
               f"CAN START MINING: {self.canStartMining}\n" \
               f"NUMBER OF TRANSACTIONS RECEIVED: {self.transactionReceivedNumber}"
