# Utils stuffs
from concurrent import futures
import logging
from time import sleep

import grpc
from multiprocessing import Process, RLock
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

    # def sendTransaction(self, request, context):
    async def sendTransaction(self, request, context):
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
        # alreadySentToMiner = request in self.receivedTransactions
        alreadySentToMiner = True

        # Final
        transactionValid = validSyntax and validSemantic and not alreadySentToMiner

        # Append to transactions
        if transactionValid:
            self.receivedTransactions.put(request)

        # if len(self.receivedTransactions) > 0:
        #     print(f"RECEIVED: {self.receivedTransactions[-1]}")
        # print(f"RECEIVED: {self.receivedTransactions.get(block=False)}")

        # Return transaction with result
        return Transaction_pb2.TransactionResponse(valid=transactionValid)


class MinerTransactionHandler(Process):
    """
    Class that handle miner transactions.
    It receive transaction and validate it

    It is the "server part" of transaction grpc protocol
    """

    def __init__(self,
                 minerConfiguration,
                 receivedTransactions,
                 lock,
                 minerCanStartToMiningCondition,
                 startTransactionNumberThreshold):
        """
        Constructor with parameters

        :param minerConfiguration: To use for finding informations about ports and other stuffs,...
        :param receivedTransactions: List of transaction received by the miner
        :param lock: Re entrant lock used to handle shared data
        :param minerCanStartToMiningCondition: Condition that permit to start mining
        :param startTransactionNumberThreshold: Condition that permit to start mining
        """

        # Init variables
        self.minerConfiguration = minerConfiguration
        self.receivedTransactions = receivedTransactions
        self.lock = lock
        self.minerCanStartToMiningCondition = minerCanStartToMiningCondition
        self.startTransactionNumberThreshold = startTransactionNumberThreshold

        # Init logging
        logging.basicConfig()

        # Init thread
        Process.__init__(self)

    async def serve(self):
        server = grpc.aio.server()
        Transaction_pb2_grpc.add_TransactionServicer_to_server(
            TransactionService(
                self.minerConfiguration,
                self.receivedTransactions,
                self.lock),
            server)
        listen_addr = f'[::]:{self.minerConfiguration.getMinerPort()}'
        server.add_insecure_port(listen_addr)
        logging.info("Starting server on %s", listen_addr)
        await server.start()
        try:
            await server.wait_for_termination()
        except KeyboardInterrupt:
            # Shuts down the server with 0 seconds of grace period. During the
            # grace period, the server won't accept new connections and allow
            # existing RPCs to continue within the grace period.
            await server.stop(0)


    def run(self):
        """
        Start server and waiting for transactions
        """
        # try:
        #     # self.lock.acquire()
        #     # Waiting because we have to arrive to the threshold of transaction to mining
        #     while len(self.receivedTransactions) > self.startTransactionNumberThreshold:
        #         self.minerCanStartToMiningCondition.wait()

        asyncio.run(self.serve())
        # except:
        #     pass

            # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            # Transaction_pb2_grpc.add_TransactionServicer_to_server(
            #     TransactionService(self.minerConfiguration,
            #                        self.receivedTransactions),
            #     server
            # )
            # server.add_insecure_port(f"[::]:{self.minerConfiguration.getMinerPort()}")
            # server.start()
            # server.wait_for_termination()
