"""
Handle the lifecycle of a miner
"""

# Utils stuffs
from threading import RLock, Condition

# Transaction maker
from comunication.mining.BlockMiningWinningHandlerServer import BlockMiningWinningHandlerServer
from comunication.transactions.TransactionHandlerMiner import MinerTransactionHandler
from mining.MinerAlgorithm import MinerAlgorithm, ProofOfLottery
from comunication.mining.BlockMiningWinningHandlerClient import BlockMiningWinningHandlerClient
from mining.runtime_mining_status.MiningStatus import MiningStatus
from mining.runtime_mining_status.MiningStatusHandler import MiningStatusHandler


def minerLifecycle(minerConfiguration):
    """
    Lifecycle of a miner

    :param minerConfiguration: Configuration to pass
    """

    # Init shared data
    miningStatus = MiningStatus(
        minerConfiguration=minerConfiguration,
        receivedTransactions=[],
        miningStartThreshold=3
    )

    # Init thread stuffs
    lock = RLock()
    canStartMiningCondition = Condition(lock)

    # Workers
    # Handle transactions (they arrive and he validate)
    minerTransactionHandler = MinerTransactionHandler(
        miningStatus=miningStatus,
        lock=lock
    )

    # Report the status and handle shared data
    miningStatusReporter = MiningStatusHandler(
        lock=lock,
        miningStatus=miningStatus,
        canStartMiningCondition=canStartMiningCondition
    )

    # Execute mining
    minerAlgorithm = MinerAlgorithm(
        miningStatus=miningStatus,
        lock=lock,
        canStartMiningCondition=canStartMiningCondition
    )

    # Listen if a block has win
    blockMiningWinningHandlerServer = BlockMiningWinningHandlerServer(
        miningStatus=miningStatus,
        lock=lock
    )

    # Comunicate that a block has win
    blockMiningWinningHandlerClient = BlockMiningWinningHandlerClient(
        lock=lock
    )

    # miningWinningHandlerClient = BlockMiningWinningHandlerClient(lock=lock)

    # Run every thread ot miner lifecycle
    # minerTransactionHandler.start()
    # miningStatusReporter.start()
    # minerAlgorithm.start()
    blockMiningWinningHandlerServer.start()
    blockMiningWinningHandlerClient.start()

    # ledgerHandler = LedgerHandler(minerConfiguration.getLedgerDatabasePath())
    # ledgerHandler.getAllEventVotedByAnAddress("event", "address")
