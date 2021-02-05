"""
Handle the lifecycle of a miner
"""

# Utils stuffs
import asyncio
from threading import RLock, Condition

# Transaction maker
from comunication.transactions.TransactionHandlerMiner import MinerTransactionHandler
from ledger_handler.LedgerHandler import LedgerHandler
from mining.MinerAlgorithm import MinerAlgorithm
from comunication.mining.BlockMiningWinningHandlerClient import MiningWinningHandlerClient

def minerLifecycle(minerConfiguration):
    """
    Lifecycle of a miner

    :param minerConfiguration: Configuration to pass
    """

    # Print informations about miner running
    print(f"Run as a miner...\n\nConfiruation:\n{minerConfiguration}\n")

    # Init shared data
    receivedTransactions = []
    lock = RLock()
    thresholdToMine = 5

    # Collect transactions and validate every single when it arrive
    minerTransactionHandler = MinerTransactionHandler(minerConfiguration=minerConfiguration,
                                                      receivedTransactions=receivedTransactions,
                                                      lock=lock,
                                                      startTransactionNumberThreshold=thresholdToMine
                                                      )

    minerAlgorithm = MinerAlgorithm(minerConfiguration=minerConfiguration,
                                    receivedTransactions=receivedTransactions,
                                    lock=lock,
                                    startTransactionNumberThreshold=thresholdToMine
                                    )

    miningWinningHandlerClient = MiningWinningHandlerClient(lock=lock)


    # Run serve and validate every transaction that arrive
    minerTransactionHandler.start()
    minerAlgorithm.start()
    miningWinningHandlerClient.start()

    # ledgerHandler = LedgerHandler(minerConfiguration.getLedgerDatabasePath())
    #ledgerHandler.getAllEventVotedByAnAddress("evento", "address")
