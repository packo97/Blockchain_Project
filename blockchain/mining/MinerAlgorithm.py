# Utils stuffs
from threading import Thread
from time import sleep

from comunication.blocks.BlockMiningObject import BlockMiningObject
from comunication.grpc_clients_handlers.BlockMiningHandlerClient import BlockMiningHandlerClient
from comunication.grpc_comunication_handlers.TransactionServiceHandler import TransactionService
#from mining.mining_utils.ProofOfLottery import ProofOfLottery
from mining.mining_utils.ProofOfLottery import ProofOfLottery


class MinerAlgorithm(Thread):
    """
    Class that handle mining algorithm.

    The main lifecycle is:
        Receiving mining requests and if there are any transaction in common (transactions already mined by me or others)
        it make symmetric difference between mined transactions and received transactions

        Wait start mining

        Calculate proof of lottery, verify it and send all to other known miners (they must verify)
        and after approbation send the request of block mining with all transactions
    """

    def __init__(self,
                 miningStatus,
                 lock,
                 canStartMiningCondition
                 ):
        """
        Constructor with parameters

        :param miningStatus: Shared current status of mining
        :param lock: Re entrant lock used to handle shared data
        :param canStartMiningCondition: Condition that told us to mining or sleep
        """

        # Init variables
        self.miningStatus = miningStatus
        self.lock = lock
        self.canStartMiningCondition = canStartMiningCondition

        # Init thread
        Thread.__init__(self)

    def run(self):
        """
        Start transaction mining.

        It wait when arrive a threshold of transactions and after start proof of lottery
        """

        while True:
            with self.lock:

                # 1) Receiving mining requests and if there are any transaction in common
                # (transactions already mined by me or others) it make symmetric difference
                # between mined transactions and received transactions

                # Remove from transaction list all transaction that other miners or me have mined
                self.removeTransactionsAlreadyMinedIfAny()

                # 2) Wait start mining

                # We are not ready to mine because we have not get the threshold
                while not self.miningStatus.canStartMining:
                    self.canStartMiningCondition.wait()

                # 3) Calculate proof of lottery, verify it and send all to other known miners (they must verify)
                # and after approbation send the request of block mining with all transactions

                # Now we can mine because we are arrived to threshold
                currentDateTime,\
                seed,\
                transactionsList,\
                blockHash,\
                lotteryFunctionBlockHash,\
                minerAddress,\
                hashedMinerAddress = ProofOfLottery.calculate(
                    minerAddress=self.miningStatus.minerConfiguration.getAddress(),
                    receivedTransactions=self.miningStatus.receivedTransactions)

                # Make verification of our work (to pickle, AUTO VERIFY)
                verify = ProofOfLottery.verify(seed=seed,
                                               receivedTransactionsStringify=transactionsList,
                                               blockHash=blockHash,
                                               lotteryFunctionBlockHash=lotteryFunctionBlockHash,
                                               minerAddress=minerAddress,
                                               hashedMinerAddress=hashedMinerAddress)

                # Get previous block hash
                from ledger_handler.LedgerHandler import LedgerHandler
                ledgerHandler = LedgerHandler(self.miningStatus.minerConfiguration.getLedgerDatabasePath())
                previousBlockHash = ledgerHandler.getPreviousBlockHash().fetchone()[0]

                # If mining go well (FOR US)
                if verify:
                    # Communicate win to miners
                    for host in self.miningStatus.minerConfiguration.getKnownHosts():
                        # Validate and re verify for each miner
                        verify = verify and BlockMiningHandlerClient\
                            .sendVictoryNotification(time=currentDateTime,
                                                     seed=seed,
                                                     transactions_list=transactionsList,
                                                     block_hash=blockHash,
                                                     lottery_number=lotteryFunctionBlockHash,
                                                     miner_address=minerAddress,
                                                     previous_block_hash=previousBlockHash,
                                                     host=host).valid

                    # FINAL verify to be pickle we use auto verification and obviously verification of other miners
                    if verify:
                        # Append my mined transactions in my block mining notifications
                        myBlockMined = BlockMiningObject(time=currentDateTime,
                                                         seed=seed,
                                                         transactionsList=transactionsList,
                                                         blockHash=blockHash,
                                                         lotteryNumber=lotteryFunctionBlockHash,
                                                         minerAddress=minerAddress,
                                                         previousBlockHash=previousBlockHash)

                        self.miningStatus.blockMiningNotificationsMinedByMe.append(myBlockMined)

                        # Flush transactions
                        self.miningStatus.receivedTransactions.clear()
                        self.miningStatus.canStartMining = False

            sleep(0.5)

    def removeTransactionsAlreadyMinedIfAny(self):
        """
        Remove all transactions from my received transactions
        that:
            other miner has mined before me
                or
            that i have previously mined
        """

        # If someone has already mined i remove transactions (if any in common)
        if self.miningStatus.anotherMinerHaveMined or self.miningStatus.iHaveMined:

            # For each block mining notification MINED BY ANOTHER
            for blockMiningNotification in self.miningStatus.blockMiningNotifications:
                # Fetch all transactions mined in mining notification
                minedByAnother = ProofOfLottery.deStringifyTransactionString(blockMiningNotification.transactionsList)

                # Symmetric difference with transactions i have
                newTransactionLists = [transaction
                                       for transaction in self.miningStatus.receivedTransactions
                                       if transaction not in minedByAnother]
                self.miningStatus.receivedTransactions = newTransactionLists

            # For each block mining notification MINED BY ME
            for blockMiningNotification in self.miningStatus.blockMiningNotificationsMinedByMe:
                # Fetch all transactions mined in mining notification
                minedByMe = ProofOfLottery.deStringifyTransactionString(blockMiningNotification.transactionsList)

                # Symmetric difference with transactions i have
                newTransactionLists = [transaction
                                       for transaction in self.miningStatus.receivedTransactions
                                       if transaction not in minedByMe]
                self.miningStatus.receivedTransactions = newTransactionLists

            # If i'm below threshold to mine
            if len(self.miningStatus.receivedTransactions) < self.miningStatus.miningStartThreshold:
                self.miningStatus.canStartMining = False

            # Remove block mining notifications
            #self.miningStatus.blockMiningNotifications.clear()
            #self.miningStatus.anotherMinerHaveMined = False

            # Remove block mining notifications
            #self.miningStatus.blockMiningNotificationsMinedByMe.clear()
            #self.miningStatus.iHaveMined = False
