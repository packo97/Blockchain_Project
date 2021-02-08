# Utils stuffs
import grpc

from concurrent import futures
import logging

from threading import Thread

# Proto generated stuffs
from comunication.blocks.BlockMiningObject import BlockMiningObject
from comunication.grpc_protos import BlockMining_pb2_grpc, BlockMining_pb2


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
        # ... Validate request using verify of ProofOfLottery class ...

        blockMiningRequestObject = BlockMiningObject(time=request.time,
                                                     seed=request.seed,
                                                     transactions_list=request.transactions_list,
                                                     block_hash=request.block_hash,
                                                     lottery_number=request.lottery_number,
                                                     miner_address=request.miner_address,
                                                     previous_block_hash=request.previous_block_hash)

        self.miningStatus.blockMiningNotifications.append(blockMiningRequestObject)

        return BlockMining_pb2.BlockMiningResponse(valid=True)
