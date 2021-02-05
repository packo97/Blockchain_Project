from threading import Thread
from time import sleep

from comunication.grpc_protos import BlockMining_pb2_grpc, BlockMining_pb2


class BlockMiningWinningHandlerClient(Thread):

    def __init__(self,lock):
        # Init thread
        Thread.__init__(self)
        self.lock = lock

    def run(self):
        while True:
            with self.lock:
                print("Ho vinto")
                sleep(3)


    def sendVictoryNotification(self, time, seed, transactions_list, transactions_hash, block_hash, lottery_number, miner_address):
        """
        Sent transaction client side

        :param time: Sending time of transaction

        :return: response
        """

        # Establish a connection channel with the host (the miner) and get response
        with grpc.insecure_channel(host) as channel:
            client = BlockMining_pb2_grpc.BlockMiningStub(channel)

            # Send transaction request and wait response
            response = client.sendVictoryNotification(
                BlockMining_pb2.BlockMiningRequest(time=time,
                                                   seed = seed,
                                                   transactions_list = transactions_list,
                                                   transactions_hash = transactions_hash,
                                                   block_hash = block_hash,
                                                   lottery_number = lottery_number,
                                                   miner_address = miner_address
                                                    )

        # If correct return true, false otherwise
        return response

