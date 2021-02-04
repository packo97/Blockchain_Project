"""
Handle the lifecycle of a miner
"""

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

    # Listen transactions while it store N>=1 transactions
    minerTransactionHandler = MinerTransactionHandler(minerConfiguration=minerConfiguration)

    # Run serve and validate every transaction that arrive
    minerTransactionHandler.serve()

    # ledgerHandler = LedgerHandler(minerConfiguration.getLedgerDatabasePath())
    #ledgerHandler.getAllEventVotedByAnAddress("evento", "address")
