# Utils stuffs
from threading import Thread
from time import sleep
import hashlib
import random
import sys


class MinerAlgorithm(Thread):
    """
    Class that handle mining algorithm
    """

    def __init__(self,
                 minerConfiguration,
                 receivedTransactions,
                 lock,
                 startTransactionNumberThreshold,
                 #minerCanStartToMiningCondition
                 ):
        """
        Constructor with parameters

        :param minerConfiguration: To use for finding informations about ports and other stuffs,...
        :param receivedTransactions: List of transaction received by the miner
        :param lock: Re entrant lock used to handle shared data
        :param startTransactionNumberThreshold: Say "start mining after you receive AT LEAST
        'startTransactionNumberThreshold' transactions"
        :param minerCanStartToMiningCondition: Condition that permit to start mining
        """

        # Init variables
        self.minerConfiguration = minerConfiguration
        self.receivedTransactions = receivedTransactions
        self.lock = lock
        self.startTransactionNumberThreshold = startTransactionNumberThreshold
        #self.minerCanStartToMiningCondition = minerCanStartToMiningCondition

        # Init thread
        Thread.__init__(self)

    def run(self):
        """
        Start transaction mining.

        It wait when arrive a threshold of transactions and after start proof of lottery
        """
        while True:
            with self.lock:
                while len(self.receivedTransactions) < self.startTransactionNumberThreshold:
                    print("wait for mining")
                    sleep(3)

                print("It's time to mine")
                print(f"{self.receivedTransactions}")

                self.proofOfLottery()
                self.receivedTransactions.clear()
                sleep(3)

    def proofOfLottery(self):
        minerAddress = hashlib.sha256(b"miner").hexdigest()
        minerLotteryNumber = self.lottery(minerAddress)

        print(f"Hash: {minerAddress} \n\tMiner lottery function: {minerLotteryNumber}")

        transactionsString = "".join(str(self.receivedTransactions))
        print(f"Transaction converted in string:\n\t{transactionsString}")

        seed = 0

        # First try
        # Transaction list converted in string + seed
        transactionsPlusSeed = str.encode(transactionsString+str(seed))
        hashTransactions = hashlib.sha256(transactionsPlusSeed).hexdigest()

        # Lottery function applied to hash
        transactionsLotteryNumber = self.lottery(hashTransactions)

        # If the first try go bad we start with seed incrementation
        while transactionsLotteryNumber!=minerLotteryNumber:
            transactionsPlusSeed = str.encode(transactionsString+str(seed))
            hashTransactions = hashlib.sha256(transactionsPlusSeed).hexdigest()
            transactionsLotteryNumber = self.lottery(hashTransactions)
            seed=seed+1

        print(f"Lottery function {transactionsLotteryNumber}    \n\tHash {hashTransactions} \n\tSeed: {seed} \n\tTransaction list plus seed: {transactionsPlusSeed.decode()}")

    def lottery(self,address):
        sum = 0

        # For each character of hash
        for i in address:
            sum = sum + ord(i)

        return sum
