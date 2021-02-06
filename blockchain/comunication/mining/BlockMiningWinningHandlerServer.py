# Utils stuffs
import grpc

from concurrent import futures
import logging

from threading import Thread

# Proto generated stuffs
from comunication.grpc_protos import BlockMining_pb2_grpc


class BlockMiningService(BlockMining_pb2_grpc.BlockMiningServicer):
    """
    Implementation of grpc BlockMiningService
    """

    def __init__(self):
        pass

    def sendVictoryNotification(self, request, context):
        print(request.transactions_list + "cacca")
        print(request)
        return BlockMining_pb2_grpc.BlockMiningResponse(valid=True)


class BlockMiningWinningHandlerServer(Thread):
    """
    Handle the communication service of block mining creation
    with grpc api on miner server side.

    On miner server side means that "miners are listening every time
    if a new block is created"
    After listening he proof that all is valid.
    In general a block is valid if:

        lottery(hash(miner_address)) = lottery(hash(block_hash)) = lottery_number
            such that: block_hash = hash(transactions_list+seed)
    """

    def __init__(self, lock, miningStatus):
        """
        Constructor with parameters

        :param lock: Re entrant lock used to handle shared data
        :param miningStatus: Shared current status of mining
        """
        self.lock = lock
        self.miningStatus = miningStatus

        # Init logging
        logging.basicConfig()

        # Init thread
        Thread.__init__(self)

    def run(self):
        """
        Start server and waiting for transactions
        """

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        BlockMining_pb2_grpc.add_BlockMiningServicer_to_server(
            BlockMiningService(),
            server
        )
        server.add_insecure_port(f"[::]:{self.miningStatus.minerConfiguration.getMinerPort()}")
        server.start()
        server.wait_for_termination()



