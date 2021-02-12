from comunication.grpc_protos import BlockStoringInLedger_pb2_grpc, BlockStoringInLedger_pb2


class BlockStoringInLedgerService(BlockStoringInLedger_pb2_grpc.BlockStoringInLedgerServicer):
    """
    Service that handle block storing in ledger notifications
    """

    def __init__(self, miningStatus):
        """
        Constructor with parameters

        :param miningStatus: Shared current status of mining
        """

        self.miningStatus = miningStatus

    def sendBlockStoringInLedgerNotification(self, request, context):
        """
        Send block storing in ledger notification service implementation

        :param request: BLock storing in ledger request
        :param context: Context to use

        :return: If block storing request is valid
        """

        # Valid
        valid = False

        # If there is only a transaction
        if len(self.miningStatus.blockMiningNotifications) == 1:
            valid = True

        # For more transactions we need to found if we have the minimum seed in block mining requests
        elif len(self.miningStatus.blockMiningNotifications) > 1:
            # All seeds of block mining requests
            seeds = [blockMiningNotification.seed for blockMiningNotification in self.miningStatus.blockStoringInLedgerNotifications ]
            minimumSeed = min(seeds)

            # We have the minimum seed
            if request.seed == minimumSeed:
                valid = True

        # Return if is valid (we have the minimum seed if there are more block mining requests)
        return BlockStoringInLedger_pb2.BlockStoringInLedgerResponse(
            valid=valid
        )
