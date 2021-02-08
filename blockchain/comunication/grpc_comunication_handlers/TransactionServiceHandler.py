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

        # # Send to other miner AT LEAST 3
        # sentToAtLeast3Miners = False
        #
        # # Count the number of sending transactions
        # sendingTransactionsCount = 0
        #
        # # Send transaction to miners (FOR EACH KNOWN HOST)
        # for minerHostAddress in self.miningStatus.minerConfiguration.getKnownHosts():
        #     try:
        #         # Get response status (try to send transaction)
        #         responseStatus = TransactionHandlerClient.sendTransaction(time=requestTransaction.time,
        #                                                                   event=requestTransaction.event,
        #                                                                   vote=requestTransaction.vote,
        #                                                                   address=requestTransaction.address,
        #                                                                   host=requestTransaction.minerHostAddress)
        #
        #         # Transaction is going well (no errors or other stuffs) we update sending transaction counter
        #         if responseStatus:
        #             sendingTransactionsCount = sendingTransactionsCount + 1
        #
        #     except Exception:
        #         print(f"{minerHostAddress} is unreachable!", file=sys.stderr)
        #
        # # Verify if transaction is sented to AT LEAST 3 peers ("3 da chiazza protocol")
        # if sendingTransactionsCount >= 3:
        #     sentToAtLeast3Miners = True

        # Final
        transactionValid = validSyntax and validSemantic and (not alreadySentToMiner) and (not alreadyVoted) # and sentToAtLeast3Miners

        # If transaction is valid we can append it to our transactions list
        if transactionValid:
            # Append to transactions
            self.miningStatus.receivedTransactions.append(requestTransaction)

        # Return transaction with result
        return Transaction_pb2.TransactionResponse(valid=transactionValid)
