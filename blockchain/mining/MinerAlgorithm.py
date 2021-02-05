# Utils stuffs
from multiprocessing import Process
from time import sleep


class MinerAlgorithm(Process):
    """
    Class that handle mining algorithm
    """

    def __init__(self,
                 minerConfiguration,
                 receivedTransactions,
                 lock,
                 startTransactionNumberThreshold,
                 minerCanStartToMiningCondition):
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
        self.minerCanStartToMiningCondition = minerCanStartToMiningCondition

        # Init thread
        Process.__init__(self)

    def run(self):
        """
        Start transaction mining.

        It wait when arrive a threshold of transactions and after start proof of lottery
        """
        while True:
            print(f"{self.receivedTransactions.empty()}")
            # print(f"\n\nsto aspettando il lock! \n{self.receivedTransactions.get(block=True)}\n\n")
            sleep(1)
            # with self.lock:
            #     if len(self.receivedTransactions) > self.startTransactionNumberThreshold:
            #         self.minerCanStartToMiningCondition.notifyAll()
            #
            #     print(len(self.receivedTransactions) <= self.startTransactionNumberThreshold)
            #     while len(self.receivedTransactions) <= self.startTransactionNumberThreshold:
            #         self.minerCanStartToMiningCondition.wait()
            #
            #     if len(self.receivedTransactions) > self.startTransactionNumberThreshold:
            #         print(self.receivedTransactions)
            #         print("Raggiunta la soglia per inizialre il mining!")
            #     else:
            #         print(self.receivedTransactions)
            #         print("Ancora non hai raggiunto la soglia!")
