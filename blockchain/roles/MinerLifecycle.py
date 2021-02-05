"""
Handle the lifecycle of a miner
"""

# Utils stuffs
from threading import RLock

# Transaction maker
from comunication.transactions.TransactionHandlerMiner import MinerTransactionHandler
from ledger_handler.LedgerHandler import LedgerHandler


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

    # Collect transactions and validate every single when it arrive
    minerTransactionHandler = MinerTransactionHandler(minerConfiguration=minerConfiguration,
                                                      receivedTransactions=receivedTransactions,
                                                      lock=lock)

    # Run serve and validate every transaction that arrive
    minerTransactionHandler.start()

    # ledgerHandler = LedgerHandler(minerConfiguration.getLedgerDatabasePath())
    #ledgerHandler.getAllEventVotedByAnAddress("evento", "address")
