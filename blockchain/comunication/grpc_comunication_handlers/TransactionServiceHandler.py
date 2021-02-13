from random import randint

from comunication.grpc_clients_handlers.TransactionHandlerClient import TransactionHandlerClient
from comunication.grpc_protos import Transaction_pb2_grpc, Transaction_pb2
from comunication.transactions.TransactionObject import TransactionObject
from comunication.transactions.validation.TransactionValidator import TransactionValidator
from ledger_handler.LedgerHandler import LedgerHandler
from mining.mining_utils.ProofOfLottery import ProofOfLottery


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
                # BROADCAST
                # If here is True, it resend transaction to others.
                # Increasing p, means decreasing probability to have True
                # We choose to manage p in this way to avoid infinite loop!
                p = 5
                useBroadcast = randint(1, 10) >= p
                responseStatus = TransactionHandlerClient.sendTransaction(time=requestTransaction.time,
                                                                          event=requestTransaction.event,
                                                                          vote=requestTransaction.vote,
                                                                          address=requestTransaction.address,
                                                                          host=minerHostAddress,
                                                                          broadcast=useBroadcast)

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

        # TRANSACTION ISN'T ALREADY SENT (bad client). You cannot send same transaction
        requestTransaction = TransactionObject(time=request.time,
                                               address=request.address,
                                               event=request.event,
                                               vote=request.vote)

        # All transaction already mined by others (NOT NOW IN LEDGER)
        alreadyMinedByOthersButNotInLedger = []
        for blockMiningNotification in self.miningStatus.blockMiningNotifications:
            alreadyMinedByOthersButNotInLedger = alreadyMinedByOthersButNotInLedger + ProofOfLottery.\
                deStringifyTransactionString(blockMiningNotification.transactionsList)

        # All transaction already mined by me (NOT NOW IN LEDGER)
        alreadyMinedByMeButNotInLedger = []
        for blockMiningNotification in self.miningStatus.blockMiningNotificationsMinedByMe:
            alreadyMinedByMeButNotInLedger = alreadyMinedByMeButNotInLedger + ProofOfLottery. \
                deStringifyTransactionString(blockMiningNotification.transactionsList)

        # TOTAL TRANSACTIONS are transaction received and transactions mined (by me or other miners that are not
        # already in the ledger)
        totalTransactions = alreadyMinedByOthersButNotInLedger + alreadyMinedByMeButNotInLedger + self.miningStatus.receivedTransactions

        # If this transaction is already sent
        alreadySentToMiner = requestTransaction in totalTransactions

        # Already voter for event. You CANNOT send (e,vote x) , (e, vote y)
        alreadyVoted = request.event in [transaction.event for transaction in totalTransactions]

        # Final
        transactionValid = validSyntax and validSemantic and (not alreadySentToMiner) and (not alreadyVoted)

        # If transaction is valid we can append it to our transactions list
        if transactionValid:
            # Sent transaction to other miners
            if request.broadcast:
                self.spreadTransactionToOtherMiners(requestTransaction)

            # Append to transactions
            if requestTransaction not in self.miningStatus.receivedTransactions:
                self.miningStatus.receivedTransactions.append(requestTransaction)

        # Return transaction with result
        return Transaction_pb2.TransactionResponse(valid=transactionValid)
