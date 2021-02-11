# Utils stuffs
from concurrent import futures
import logging
from time import sleep

import grpc
from threading import Thread, RLock
import asyncio
import sys

# Proto generated files
from comunication.grpc_clients_handlers.TransactionHandlerClient import TransactionHandlerClient
from comunication.grpc_protos import Transaction_pb2_grpc, Transaction_pb2
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

    def spreadTransactionToOtherMiners(self, requestTransaction):
        """
        Send transaction to other miners.
        Is not important if they return false
        (because they have already the transaction
            or
        they are unavailable
            or
        other stuff...)

        This is because the "three da chiazza protocol is guarantee
        client side

        :param requestTransaction: Transaction request to spread
        """

        # Send transaction to miners (FOR EACH KNOWN HOST)
        for minerHostAddress in self.miningStatus.minerConfiguration.getKnownHosts():
            try:
                # Send transaction and do nothing
                responseStatus = TransactionHandlerClient.sendTransaction(time=requestTransaction.time,
                                                                          event=requestTransaction.event,
                                                                          vote=requestTransaction.vote,
                                                                          address=requestTransaction.address,
                                                                          host=requestTransaction.minerHostAddress)

            # In case of exception do nothing
            except Exception:
                pass

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

        # If transaction is valid we can append it to our transactions list
        if transactionValid:
            # Sent transaction to other miners
            self.spreadTransactionToOtherMiners(requestTransaction)

            # Append to transactions
            self.miningStatus.receivedTransactions.append(requestTransaction)

        # Return transaction with result
        return Transaction_pb2.TransactionResponse(valid=transactionValid)
