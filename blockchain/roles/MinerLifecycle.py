"""
Handle the lifecycle of a miner
"""

# Utils stuffs
from threading import RLock, Condition

# Transaction maker
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

    # minerAddress = miningStatus.minerConfiguration.getAddress()
    # print(ProofOfLottery.calculate(minerAddress, ["prova", "prova1"]))
    # exit(1)

    lock = RLock()
    canStartMiningCondition = Condition(lock)

    # Collect transactions and validate every single when it arrive
    minerTransactionHandler = MinerTransactionHandler(
        miningStatus=miningStatus,
        lock=lock
    )

    miningStatusReporter = MiningStatusHandler(
        lock=lock,
        miningStatus=miningStatus,
        canStartMiningCondition=canStartMiningCondition
    )

    minerAlgorithm = MinerAlgorithm(
        miningStatus=miningStatus,
        lock=lock,
        canStartMiningCondition=canStartMiningCondition
    )

    # miningWinningHandlerClient = BlockMiningWinningHandlerClient(lock=lock)

    # Run every thread ot miner lifecycle
    minerTransactionHandler.start()
    miningStatusReporter.start()
    minerAlgorithm.start()
    # miningWinningHandlerClient.start()

    # ledgerHandler = LedgerHandler(minerConfiguration.getLedgerDatabasePath())
    # ledgerHandler.getAllEventVotedByAnAddress("event", "address")
