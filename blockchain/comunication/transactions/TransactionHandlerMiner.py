# Utils stuffs
from concurrent import futures
import logging
import grpc

# Proto generated files
from comunication.grpc_protos import Transaction_pb2_grpc, Transaction_pb2


class TransactionService(Transaction_pb2_grpc.TransactionServicer):

    def sendTransaction(self, request, context):
        return Transaction_pb2.TransactionResponse(valid=True)


class MinerTransactionHandler:

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        Transaction_pb2_grpc.add_TransactionServicer_to_server(TransactionService(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()


    def __init__(self):
        print("Miner")
        logging.basicConfig()
        self.serve()
