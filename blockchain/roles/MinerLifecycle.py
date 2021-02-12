"""
Handle the lifecycle of a miner
"""

# Utils stuffs
from threading import RLock, Condition

# Transaction maker
from comunication.grpc_comunication_handlers.GrpcServerHandler import GrpcServerHandler

# Mining algorithm
from mining.MinerAlgorithm import MinerAlgorithm

# Mining current status
from mining.mining_notifications.MiningNotificationsHandler import MiningNotificationsHandler
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

    # Select what is the "best" mining notification that must be stored in ledger
    miningNotificationsHandler = MiningNotificationsHandler(
        miningStatus=miningStatus,
        lock=lock
    )

    # Run every thread ot miner lifecycle
    grpcServerHandler.start()
    miningStatusReporter.start()
    minerAlgorithm.start()
    miningNotificationsHandler.start()
