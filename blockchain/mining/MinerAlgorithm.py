# Utils stuffs
from datetime import datetime
from threading import Thread
from time import sleep
import hashlib
import random
import sys

from comunication.blocks.BlockMiningObject import BlockMiningObject
from comunication.grpc_clients_handlers.BlockMiningHandlerClient import BlockMiningHandlerClient
from comunication.transactions.TransactionObject import TransactionObject


class ProofOfLottery:
    """
    Implementation of proof of lottery
    with validation.
    Useful in two sides:
        When miner do proof of lottery
        When miner approve the proof of lottery of other miners
    """

    @staticmethod
    def stringifyTransactionList(transactionList):
        """
        Stringify a list of transaction

        :param transactionList: Transaction list to stringify
        :return: String encoding of transactions
        """

        return ''.join(str(transaction) for transaction in transactionList)

    @staticmethod
    def deStringifyTransactionString(transactionListAsString):
        """
        Transform a string (that express a list of transactions)
        in a list of TransactionObject.

        It is useful because permit us to make simmetric difference
        with respect to transactions we have.
        Is possible in fact that a miner can mine before us a transactions
        that we need to mine

        :param transactionListAsString: List of transactions expressed as string

        :return: List of TransactionObject
        """

        # Split by | and remove last element (because | is at the end and last one is empty)
        transactionStringAsList = transactionListAsString.split('|')
        transactionStringAsList.pop()

        # List of transactions objects
        transactionObjectList = []

        # Enumerate transactions
        for transaction in transactionStringAsList:
            # Split transaction (0->timestamp, 1->address, 2->event, 3->vote)
            item = transaction.split(';')
            transactionObjectList.append(TransactionObject(item[0], item[1], item[2], item[3]))

        return transactionObjectList

    @staticmethod
    def lottery(hashString):
        """
        Calculate lottery function over a hash string

        :param hashString: Hash over calculate lottery function

        :return: Lottery number
        """

        # Sum all
        return sum(
            # List all
            list(map(ord, hashString))
        )

    @staticmethod
    def verify(seed,
               receivedTransactionsStringify,
               blockHash,
               lotteryFunctionBlockHash,
               minerAddress,
               hashedMinerAddress):
        """
        Verify if block is validate correctly by a miner

        :return: True if yes, False if not
        """

        # Verify that hashed miner address is not created "as art"
        correctMinerAddress = (hashlib.sha256(str.encode(minerAddress)).hexdigest() == hashedMinerAddress)

        # Lottery is correct the same on hashed miner address and on lotteryFunctionBlockHash
        correctLottery = (ProofOfLottery.lottery(hashedMinerAddress) == lotteryFunctionBlockHash)

        # Correct calculated block hash
        receivedTransactionsConcatSeed = receivedTransactionsStringify + str(seed)
        correctBlockHash = (blockHash == hashlib.sha256(str.encode(receivedTransactionsConcatSeed)).hexdigest())

        # Return final verify
        return correctMinerAddress and correctLottery and correctBlockHash

    @staticmethod
    def calculate(minerAddress, receivedTransactions):
        """
        Calculate Proof Of Lottery

        :param minerAddress: Address of miner who do the proof of lottery
        :param receivedTransactions: List of received received

        :return:
        """

        # hashed miner address
        hashedMinerAddress = hashlib.sha256(str.encode(minerAddress)).hexdigest()

        # Lottery function over miner
        lotteryFunctionOnMinerAddress = ProofOfLottery.lottery(hashedMinerAddress)

        # Stringify transactions
        receivedTransactionsStringify = ProofOfLottery.stringifyTransactionList(receivedTransactions)

        # Main loop
        foundCorrectSeed = False
        seed = 0
        while not foundCorrectSeed:
            # Update seed RANDOMLY
            seed = random.randint(0, sys.maxsize)

            # Concatenate received transaction string with seed
            receivedTransactionsConcatSeed = receivedTransactionsStringify + str(seed)

            # Try to construct block hash using seed and transactions
            blockHash = hashlib.sha256(str.encode(receivedTransactionsConcatSeed)).hexdigest()

            # Condition of winning
            lotteryFunctionBlockHash = ProofOfLottery.lottery(blockHash)
            if lotteryFunctionBlockHash == lotteryFunctionOnMinerAddress:
                foundCorrectSeed = True

        # When block is mined
        currentDateTime = datetime.now().strftime("%d/%m/%Y,%H:%M:%S")

        # Return useful data to create new block
        return currentDateTime, seed, receivedTransactionsStringify, blockHash, lotteryFunctionBlockHash, minerAddress, hashedMinerAddress


class MinerAlgorithm(Thread):
    """
    Class that handle mining algorithm.

    The main lifecycle is:
        Receiving mining requests and if there are any transaction in common (transactions already mined)
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
                # (transactions already mined) it make symmetric difference between mined
                # transactions and received transactions

                # Remove from transaction list all transaction that other miners have mined
                self.removeTransactionsAlreadyMinedIfAny()

                # 2) Wait start mining

                # We are not ready to mine because we have not get the threshold
                while not self.miningStatus.canStartMining:
                    self.canStartMiningCondition.wait()

                # 3) Calculate proof of lottery, verify it and send all to other known miners (they must verify)
                # and after approbation send the request of block mining with all transactions

                # Now we can mine because we are arrived to threshold
                proofOfLotteryResult = ProofOfLottery\
                    .calculate(minerAddress=self.miningStatus.minerConfiguration.getAddress(),
                               receivedTransactions=self.miningStatus.receivedTransactions)

                # Make verification of our work (to pickle, AUTO VERIFY)
                verify = ProofOfLottery.verify(seed=proofOfLotteryResult[1],
                                               receivedTransactionsStringify=proofOfLotteryResult[2],
                                               blockHash=proofOfLotteryResult[3],
                                               lotteryFunctionBlockHash=proofOfLotteryResult[4],
                                               minerAddress=proofOfLotteryResult[5],
                                               hashedMinerAddress=proofOfLotteryResult[6])

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
                            .sendVictoryNotification(time=proofOfLotteryResult[0],
                                                     seed=str(proofOfLotteryResult[1]),
                                                     transactions_list=proofOfLotteryResult[2],
                                                     block_hash=proofOfLotteryResult[3],
                                                     lottery_number=str(proofOfLotteryResult[4]),
                                                     miner_address=proofOfLotteryResult[5],
                                                     previous_block_hash=str(previousBlockHash),
                                                     host=host)

                    # Final verify to be pickle we use auto verification and obviously verification of other miners
                    if verify and not self.miningStatus.anotherMinerHaveMined:
                        # Insert block in ledger
                        ledgerHandler.insertBlockInLedger(
                            BlockMiningObject(time=proofOfLotteryResult[0],
                                              seed=str(proofOfLotteryResult[1]),
                                              transactions_list=proofOfLotteryResult[2],
                                              block_hash=proofOfLotteryResult[3],
                                              lottery_number=str(proofOfLotteryResult[4]),
                                              miner_address=proofOfLotteryResult[5],
                                              previous_block_hash=str(previousBlockHash)
                                              )
                        )

                        # Flush transactions list
                        self.miningStatus.receivedTransactions.clear()
                        self.miningStatus.canStartMining = False

                        # Flush block mining request
                        self.miningStatus.blockMiningNotifications = []
                        self.miningStatus.anotherMinerHaveMined = False

            sleep(0.5)

    def removeTransactionsAlreadyMinedIfAny(self):
        """
        Remove all transactions from my received transactions
        that other miner has mined before me
        """

        # If someone has already mined i remove transactions (if any in common)
        if self.miningStatus.anotherMinerHaveMined:

            # For each block mining notification
            for blockMiningNotification in self.miningStatus.blockMiningNotifications:
                # Fetch all transactions mined in mining notification
                minedByAnother = ProofOfLottery.deStringifyTransactionString(blockMiningNotification.transactions_list)

                # Symmetric difference with transactions i have
                newTransactionLists = [transaction
                                       for transaction in self.miningStatus.receivedTransactions
                                       if transaction not in minedByAnother]
                self.miningStatus.receivedTransactions = newTransactionLists

            # If i'm below threshold to mine
            if len(self.miningStatus.receivedTransactions) < self.miningStatus.miningStartThreshold:
                self.miningStatus.canStartMining = False

            # Remove block mining notifications
            self.miningStatus.blockMiningNotifications = []
            self.miningStatus.anotherMinerHaveMined = False
