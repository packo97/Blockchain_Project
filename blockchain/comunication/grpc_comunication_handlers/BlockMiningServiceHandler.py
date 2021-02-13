from comunication.blocks.BlockMiningObject import BlockMiningObject
from comunication.grpc_protos import BlockMining_pb2_grpc, BlockMining_pb2
from mining.mining_utils.ProofOfLottery import ProofOfLottery


class BlockMiningService(BlockMining_pb2_grpc.BlockMiningServicer):
    """
    Service used by grpc python implementation

    A miner receive the block mining request and validate it.
    If validation stuffs is ok
    """

    def __init__(self, miningStatus):
        """
        Constructor with parameters

        :param miningStatus: Shared current status of mining
        """

        self.miningStatus = miningStatus

    def sendVictoryNotification(self, request, context):
        """
        Send victory notification service function implementation

        :param request: Request to send
        :param context: Context
        :return: If is valid
        """

        # Create block mining object
        blockMiningRequestObject = BlockMiningObject(time=request.time,
                                                     seed=request.seed,
                                                     transactionsList=request.transactions_list,
                                                     blockHash=request.block_hash,
                                                     lotteryNumber=request.lottery_number,
                                                     minerAddress=request.miner_address,
                                                     previousBlockHash=request.previous_block_hash)

        # Verify block mining
        verified = ProofOfLottery.verify(seed=blockMiningRequestObject.seed,
                                         receivedTransactionsStringify=blockMiningRequestObject.transactionsList,
                                         blockHash=blockMiningRequestObject.blockHash,
                                         lotteryFunctionBlockHash=blockMiningRequestObject.lotteryNumber,
                                         minerAddress=blockMiningRequestObject.minerAddress,
                                         hashedMinerAddress=blockMiningRequestObject.hashedMinerAddress)

        # Append to list of received if is correct
        if verified:
            self.miningStatus.blockMiningNotifications.append(blockMiningRequestObject)

        return BlockMining_pb2.BlockMiningResponse(valid=verified)
