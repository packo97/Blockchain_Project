from concurrent import futures
import logging

from threading import Thread
from time import sleep

from comunication.grpc_protos import BlockMining_pb2_grpc

import grpc


class BlockMiningService(BlockMining_pb2_grpc.BlockMiningServicer):
    """
    Service used by grpc python implementation

    A miner receive transactions and validate it.
    It transaction are valid (sintattically and semantically)
    """

    def __init__(self):
        pass

    def sendVictoryNotification(self, request, context):
        return BlockMining_pb2_grpc.BlockMiningResponse(valid=True)


class BlockMiningWinningHandlerMiner(Thread):

    def __init__(self,lock):

        self.lock = lock

        # Init logging
        logging.basicConfig()

        # Init thread
        Thread.__init__(self)


    def run(self):
        """
        Start server and waiting for transactions
        """

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        BlockMining_pb2_grpc.add_TransactionServicer_to_server(
            BlockMiningService(
                # pass paremeters
            ),
            server
        )
        server.add_insecure_port(f"[::]:{self.minerConfiguration.getMinerPort()}")
        server.start()
        server.wait_for_termination()



