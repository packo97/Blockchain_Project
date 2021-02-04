# Utils stuffs
from concurrent import futures
import logging
import grpc

# Proto generated files
from comunication.grpc_protos import Transaction_pb2_grpc, Transaction_pb2


class TransactionService(Transaction_pb2_grpc.TransactionServicer):
    """
    Service used by grpc python implementation
    """
    def sendTransaction(self, request, context):
        return Transaction_pb2.TransactionResponse(valid=True)


class MinerTransactionHandler:
    """
    Class that handle miner transactions.

    It is the "server part" of transaction grpc protocol
    """

    def serve(self):
        """
        Start server and waiting for transactions
        """
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        Transaction_pb2_grpc.add_TransactionServicer_to_server(TransactionService(), server)
        server.add_insecure_port(f"[::]:{self.minerConfiguration.getMinerPort()}")
        server.start()
        server.wait_for_termination()

    def __init__(self, minerConfiguration):
        """
        Constructor with parameters

        :param minerConfiguration: To use for finding informations about ports and other stuffs,...
        """

        # Init variables
        self.minerConfiguration = minerConfiguration

        # Init logging
        logging.basicConfig()
        # self.serve()
