# Utils stuffs
from concurrent import futures
import logging
from time import sleep

import grpc
from threading import Thread, RLock
import asyncio

# Proto generated files
from comunication.grpc_protos import Transaction_pb2_grpc, Transaction_pb2
from comunication.grpc_protos.Transaction_pb2_grpc import Transaction
from comunication.transactions.TransactionObject import TransactionObject
from comunication.transactions.validation.TransactionValidator import TransactionValidator
from ledger_handler.LedgerHandler import LedgerHandler


class TransactionService(Transaction_pb2_grpc.TransactionServicer):
    """
    Service used by grpc python implementation

    A miner receive transactions and validate it.
    It transaction are valid (sintattically and semantically)
    """

    def __init__(self, miningStatus):
        """
        Constructor with parameters

        :param miningStatus: Shared current status of mining
        """

        self.miningStatus = miningStatus

    def sendTransaction(self, request, context):
        # By default we assume transaction false
        transactionValid = False

        # ... Validation ...
        # FORMAT (syntax)
        validFormatVote = TransactionValidator.isTransactionFormatValid(event=request.event, vote=request.vote)
        validSyntax = validFormatVote[0] and validFormatVote[1]

        # LEDGER (semantic)
        ledgerHandler = LedgerHandler(self.miningStatus.minerConfiguration.getLedgerDatabasePath())
        eventVoted = ledgerHandler.getAllEventVotedByAnAddress(address=request.address, event=request.event)
        validSemantic = eventVoted.fetchone() is None

        # Transaction is already sent (bad client)
        requestTransaction = TransactionObject(time=request.time,
                                               address=request.address,
                                               event=request.event,
                                               vote=request.vote)
        alreadySentToMiner = requestTransaction in self.miningStatus.receivedTransactions

        # Already voter for event
        alreadyVoted = request.event in [transaction.event for transaction in self.miningStatus.receivedTransactions]

        # Final
        transactionValid = validSyntax and validSemantic and (not alreadySentToMiner) and (not alreadyVoted)

        # Append to transactions
        if transactionValid:
            self.miningStatus.receivedTransactions.append(requestTransaction)

        # Return transaction with result
        return Transaction_pb2.TransactionResponse(valid=transactionValid)


class MinerTransactionHandler(Thread):
    """
    Class that handle miner transactions.
    It receive transaction and validate it

    It is the "server part" of transaction grpc protocol
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
        Transaction_pb2_grpc.add_TransactionServicer_to_server(
            TransactionService(self.miningStatus),
            server
        )
        server.add_insecure_port(f"[::]:{self.miningStatus.minerConfiguration.getMinerPort()}")
        server.start()
        server.wait_for_termination()
