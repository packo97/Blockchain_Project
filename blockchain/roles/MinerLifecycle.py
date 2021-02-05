"""
Handle the lifecycle of a miner
"""

# Utils stuffs
import asyncio
from multiprocessing import RLock, Condition, Queue

# Transaction maker
from comunication.transactions.TransactionHandlerMiner import MinerTransactionHandler
from ledger_handler.LedgerHandler import LedgerHandler
from mining.MinerAlgorithm import MinerAlgorithm


def minerLifecycle(minerConfiguration):
    """
    Lifecycle of a miner

    :param minerConfiguration: Configuration to pass
    """

    # Print informations about miner running
    print(f"Run as a miner...\n\nConfiruation:\n{minerConfiguration}\n")

    # Init shared data
    receivedTransactions = Queue()
    lock = RLock()
    startTransactionNumberThreshold = 1

    # Useful conditions
    # Condition that say "now we have get the threshold of transactions N and we can start minig"
    minerCanStartToMiningCondition = Condition(lock)

    # Collect transactions and validate every single when it arrive
    minerTransactionHandler = MinerTransactionHandler(minerConfiguration=minerConfiguration,
                                                      receivedTransactions=receivedTransactions,
                                                      lock=lock,
                                                      minerCanStartToMiningCondition=minerCanStartToMiningCondition,
                                                      startTransactionNumberThreshold=startTransactionNumberThreshold)

    minerAlgorithm = MinerAlgorithm(minerConfiguration=minerConfiguration,
                                    receivedTransactions=receivedTransactions,
                                    lock=lock,
                                    startTransactionNumberThreshold=startTransactionNumberThreshold,
                                    minerCanStartToMiningCondition=minerCanStartToMiningCondition)

    # Run serve and validate every transaction that arrive
    # asyncio.run(minerTransactionHandler.serve())
    minerTransactionHandler.start()
    minerAlgorithm.start()

    # ledgerHandler = LedgerHandler(minerConfiguration.getLedgerDatabasePath())
    #ledgerHandler.getAllEventVotedByAnAddress("evento", "address")
