# Utils stuffs
from concurrent import futures
import logging
from time import sleep

import grpc
from threading import Thread, RLock
import asyncio

# Proto generated files
from comunication.grpc_protos import Transaction_pb2_grpc, Transaction_pb2
from comunication.transactions.validation.TransactionValidator import TransactionValidator
from ledger_handler.LedgerHandler import LedgerHandler


class TransactionService(Transaction_pb2_grpc.TransactionServicer):
    """
    Service used by grpc python implementation

    A miner receive transactions and validate it.
    It transaction are valid (sintattically and semantically)
    """

    def __init__(self, minerConfiguration, receivedTransactions, lock):
        """
        Constructor with parameters

        :param minerConfiguration: To use for finding informations about ports and other stuffs,...
        :param receivedTransactions: List of transaction received by the miner
        """

        self.minerConfiguration = minerConfiguration
        self.receivedTransactions = receivedTransactions
        self.lock = lock

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
        alreadySentToMiner = request in self.receivedTransactions

        # Final
        transactionValid = validSyntax and validSemantic and not alreadySentToMiner

        # Append to transactions
        if transactionValid:
            self.receivedTransactions.append(request)

        # if len(self.receivedTransactions) > 0:
        #     print(f"RECEIVED: {self.receivedTransactions[-1]}")
        # print(f"RECEIVED: {self.receivedTransactions.get(block=False)}")

        # Return transaction with result
        return Transaction_pb2.TransactionResponse(valid=transactionValid)


class MinerTransactionHandler(Thread):
    """
    Class that handle miner transactions.
    It receive transaction and validate it

    It is the "server part" of transaction grpc protocol
    """

    def __init__(self,
                 minerConfiguration,
                 receivedTransactions,
                 lock,
                 startTransactionNumberThreshold):
        """
        Constructor with parameters

        :param minerConfiguration: To use for finding informations about ports and other stuffs,...
        :param receivedTransactions: List of transaction received by the miner
        :param lock: Re entrant lock used to handle shared data
        :param startTransactionNumberThreshold: Condition that permit to start mining
        """

        # Init variables
        self.minerConfiguration = minerConfiguration
        self.receivedTransactions = receivedTransactions
        self.lock = lock
        self.startTransactionNumberThreshold = startTransactionNumberThreshold

        # Init logging
        logging.basicConfig()

        # Init thread
        Thread.__init__(self)

    def run(self):
        """
        Start server and waiting for transactions
        """

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        Transaction_pb2_grpc.add_TransactionServicer_to_server(
            TransactionService(self.minerConfiguration,
                               self.receivedTransactions,
                               self.lock),
            server
        )
        server.add_insecure_port(f"[::]:{self.minerConfiguration.getMinerPort()}")
        server.start()
        server.wait_for_termination()
