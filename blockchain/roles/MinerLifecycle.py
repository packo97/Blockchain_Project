"""
Handle the lifecycle of a miner
"""

# Transaction maker
from comunication.transactions.TransactionHandlerMiner import MinerTransactionHandler


def minerLifecycle(minerConfiguration):
    """
    Lifecycle of a miner

    :param minerConfiguration: Configuration to pass
    """
    print(f"Run as a miner...\n\nConfiruation:\n{minerConfiguration}\n")
    s = MinerTransactionHandler()
