# Utils stuffs
from concurrent import futures
import logging
import grpc

# Proto generated files
from comunication.grpc_protos import Transaction_pb2_grpc, Transaction_pb2
from comunication.transactions import minerReceivedTransactions
from comunication.transactions.validation.TransactionValidator import TransactionValidator
from ledger_handler.LedgerHandler import LedgerHandler


class TransactionService(Transaction_pb2_grpc.TransactionServicer):
    """
    Service used by grpc python implementation

    A miner receive transactions and validate it.
    It transaction are valid (sintattically and semantically)
    """

    def __init__(self, minerConfiguration):
        self.minerConfiguration = minerConfiguration

    def sendTransaction(self, request, context):
        # By default we assume transaction false
        transactionValid = False

        # ... Validation ...
        # FORMAT (syntax)
        validFormatVote = TransactionValidator.isTransactionFormatValid(event=request.event, vote=request.vote)
        validSyntax = validFormatVote[0] and validFormatVote[1]

        # LEDGER (semantic)
        ledgerHandler = LedgerHandler(self.minerConfiguration.getLedgerDatabasePath())
        eventVoted = ledgerHandler.getAllEventVotedByAnAddress(address=request.address, event=request.event)
        validSemantic = eventVoted.fetchone() is None

        # Transaction is already sent (bad client)
        alreadySentToMiner = request in minerReceivedTransactions

        # Final
        transactionValid = validSyntax and validSemantic and not alreadySentToMiner

        # Append to transactions
        if transactionValid:
            minerReceivedTransactions.append(request)

        # Return transaction with result
        return Transaction_pb2.TransactionResponse(valid=transactionValid)


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
        Transaction_pb2_grpc.add_TransactionServicer_to_server(TransactionService(self.minerConfiguration), server)
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