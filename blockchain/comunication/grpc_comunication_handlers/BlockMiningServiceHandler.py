# Utils stuffs
import grpc

from concurrent import futures
import logging

from threading import Thread

# Proto generated stuffs
from comunication.grpc_protos import BlockMining_pb2_grpc


class BlockMiningService(BlockMining_pb2_grpc.BlockMiningServicer):
    """
    Service used by grpc python implementation

    A miner receive the block mining request and validate it.
    If validation stuffs is ok
    """

    def __init__(self):
        pass

    def sendVictoryNotification(self, request, context):
        # ... Validate request using verify of ProofOfLottery class ...
        print(request)
        return BlockMining_pb2_grpc.BlockMiningResponse(valid=True)
