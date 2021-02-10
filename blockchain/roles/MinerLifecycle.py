"""
Handle the lifecycle of a miner
"""

# Utils stuffs
from threading import RLock, Condition

# Transaction maker
from comunication.grpc_comunication_handlers.GrpcServerHandler import GrpcServerHandler
from mining.BlockMiningReceiverHandler import BlockMiningReceiverHandler

from mining.MinerAlgorithm import MinerAlgorithm
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
    # Server thath handle grpc requests
    grpcServerHandler = GrpcServerHandler(
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

    # Monitor if block mining notifications arrived and eventually update mining status
    # blockMiningReceiverHandler = BlockMiningReceiverHandler(
    #     miningStatus=miningStatus,
    #     lock=lock
    # )

    # Run every thread ot miner lifecycle
    grpcServerHandler.start()
    miningStatusReporter.start()
    minerAlgorithm.start()
    # blockMiningReceiverHandler.start()
