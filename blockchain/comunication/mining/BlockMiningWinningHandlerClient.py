# Utils stuffs
from threading import Thread
from time import sleep

# Proto generated stuffs
from comunication.grpc_protos import BlockMining_pb2_grpc, BlockMining_pb2


class BlockMiningWinningHandlerClient(Thread):
    """
    Handle the block mining communication part client-side.

    When a client (a miner) win, he need to told it to other miners!
    """

    def __init__(self, lock):
        """
        Constructor with parameters

        :param lock: Re entrant lock used to handle shared data
        """

        # Init re entrant lock
        self.lock = lock

        # Init thread
        Thread.__init__(self)

    def run(self):
        """
        Thread lifecycle
        """

        while True:
            with self.lock:
                print("Ho vinto")
                sleep(3)

    def sendVictoryNotification(self,
                                time,
                                seed,
                                transactions_list,
                                transactions_hash,
                                block_hash,
                                lottery_number,
                                miner_address,
                                previous_block_hash):
        """
        Used by a miner to told to other miners that
        "he has winning mineing game"

        :param time: Time in which block is mined
        :param seed: seed used in proof of lottery
        :param transactions_list: List of transactions contained in the block
        :param transactions_hash: Hash of transactions (merkle)
        :param block_hash: Hash of block
        :param lottery_number: Lottery number obtained by lottery(hash(block_hash))
        :param miner_address: Address of miner that mine block
        :param previous_block_hash: Hash of previous block

        :return: If mining go well or not
        The verification is very easy:

            lottery(hash(miner_address)) = lottery(hash(block_hash)) = lottery_number,
                such that: block_hash = hash(transactions_list+seed)
        """

        # Establish a connection channel with the host (the miner) and get response
        with grpc.insecure_channel(host) as channel:
            client = BlockMining_pb2_grpc.BlockMiningStub(channel)

            # Send transaction request and wait response
            response = client.sendVictoryNotification(
                BlockMining_pb2.BlockMiningRequest(time=time,
                                                   seed=seed,
                                                   transactions_list=transactions_list,
                                                   transactions_hash=transactions_hash,
                                                   block_hash=block_hash,
                                                   lottery_number=lottery_number,
                                                   miner_address=miner_address,
                                                   previous_block_hash=previous_block_hash
                                                   ))

        # If correct return true, false otherwise
        return response

