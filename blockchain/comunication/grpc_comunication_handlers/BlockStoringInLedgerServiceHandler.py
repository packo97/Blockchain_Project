from comunication.grpc_protos import BlockStoringInLedger_pb2_grpc


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
        pass