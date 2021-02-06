# Utils stuffs
from datetime import datetime
from threading import Thread
from time import sleep
import hashlib
import random
import sys


class ProofOfLottery:

    @staticmethod
    def stringifyTransactionList(transactionList):
        return ''.join(str(transaction) for transaction in transactionList)

    @staticmethod
    def calculate(minerAddress, receivedTransactions):
        # hashed miner address
        hashedMinerAddress = hashlib.sha256(str.encode(minerAddress)).hexdigest()

        # Stringify transactions
        receivedTransactionsString = ProofOfLottery.stringifyTransactionList(receivedTransactions)

        return hashedMinerAddress, receivedTransactionsString



class MinerAlgorithm(Thread):
    """
    Class that handle mining algorithm
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
                # we are not ready to mine because we have not get the threshold
                while not self.miningStatus.canStartMining:
                    self.canStartMiningCondition.wait()

                # now we can mine because we arrived to threshold
                self.proofOfLottery()

                # ... Communicate solution to all ...

                # Flush transaction list
                self.miningStatus.receivedTransactions.clear()

    def proofOfLottery(self):
        """
        Proof og lottery main cycle function

        :return: All useful informations of a block mined
        """

        # Miner address hashed
        address = str.encode(self.miningStatus.minerConfiguration.getAddress())
        minerAddress = hashlib.sha256(address).hexdigest()

        # Lottery function on miner address function
        minerLotteryNumber = self.lottery(minerAddress)

        # our merkle
        transactionsString = self.hashingTransactions(self.miningStatus.receivedTransactions)

        seed = 0

        # START ALGORITHM - First try

        # Transaction list converted in string + seed
        transactionsPlusSeed = str.encode(transactionsString+str(seed))
        hashTransactions = hashlib.sha256(transactionsPlusSeed).hexdigest()

        # Lottery function applied to hash
        transactionsLotteryNumber = self.lottery(hashTransactions)

        # If the first try go bad we start with seed incrementation
        while transactionsLotteryNumber != minerLotteryNumber:
            # Increment seed
            seed = seed + 1

            # Step ... N ...
            transactionsPlusSeed = str.encode(transactionsString+str(seed))
            hashTransactions = hashlib.sha256(transactionsPlusSeed).hexdigest()
            transactionsLotteryNumber = self.lottery(hashTransactions)

        # Return all useful data

        return datetime.now(), seed, transactionsString,

    def lottery(self, address):
        # Sum all
        return sum(
            # List all
            list(
                # Map ord function to each character of address
                map(ord, address)
            )
        )

    def hashingTransactions(self, transactions):
        # we have to implement markle algorithm
        return "".join(str(transactions))
