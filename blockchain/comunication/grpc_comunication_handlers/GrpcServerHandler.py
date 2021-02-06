# Cuncurrency stuff
from concurrent import futures
import logging
from threading import Thread

# Grpc Stuff
from comunication.grpc_protos import Transaction_pb2_grpc, BlockMining_pb2_grpc
import grpc

# Services
from comunication.grpc_comunication_handlers.BlockMiningServiceHandler import BlockMiningService
from comunication.grpc_comunication_handlers.TransactionServiceHandler import TransactionService


class GrpcServerHandler(Thread):
    """
    Class that handle grpc server

    It receive transactions, block mining requests, ...
    """

    def __init__(self,
                 miningStatus,
                 lock):
        """
        Constructor with parameters

        :param miningStatus: Shared current status of mining
        :param lock: Re entrant lock used to handle shared data
        """

        # Init variables
        self.miningStatus = miningStatus
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

        # Add transaction service
        Transaction_pb2_grpc.add_TransactionServicer_to_server(
            TransactionService(self.miningStatus),
            server
        )

        # Add block mining service
        BlockMining_pb2_grpc.add_BlockMiningServicer_to_server(
            BlockMiningService(),
            server
        )

        # Start server
        server.add_insecure_port(f"[::]:{self.miningStatus.minerConfiguration.getMinerPort()}")
        server.start()
        server.wait_for_termination()
