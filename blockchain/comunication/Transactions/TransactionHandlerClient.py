# Utils stuffs
from concurrent import futures
import logging
import grpc

# Proto generated files
from comunication.grpc_protos import Transaction_pb2_grpc, Transaction_pb2


class ClientTransactionHandler:
    """
    Handle transaction by client view (client must only to send transactions)
    """

    def __init__(self):
        """
        Constructor without parameters
        """
        print("Client")
        logging.basicConfig()

    def sendTransaction(self, time, address, event, vote):
        with grpc.insecure_channel('localhost:50051') as channel:
            client = Transaction_pb2_grpc.TransactionStub(channel)
            response = client.sendTransaction(Transaction_pb2.TransactionRequest(time=time, address=address, event=event, vote=vote))

        return response
