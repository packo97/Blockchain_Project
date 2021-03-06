from datetime import datetime
import hashlib
import random
import sys

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
        correctLottery = (ProofOfLottery.lottery(hashedMinerAddress) == int(lotteryFunctionBlockHash))

        # Correct calculated block hash
        receivedTransactionsConcatSeed = receivedTransactionsStringify + seed
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
            stringifySeed = str(seed)
            receivedTransactionsConcatSeed = receivedTransactionsStringify + stringifySeed

            # Try to construct block hash using seed and transactions
            blockHash = hashlib.sha256(str.encode(receivedTransactionsConcatSeed)).hexdigest()

            # Condition of winning
            lotteryFunctionBlockHash = ProofOfLottery.lottery(blockHash)
            if lotteryFunctionBlockHash == lotteryFunctionOnMinerAddress:
                foundCorrectSeed = True

        # When block is mined
        currentDateTime = datetime.now().strftime("%d/%m/%Y,%H:%M:%S")

        # Return useful data to create new block
        return currentDateTime, stringifySeed, receivedTransactionsStringify, blockHash, str(lotteryFunctionBlockHash), minerAddress, hashedMinerAddress
