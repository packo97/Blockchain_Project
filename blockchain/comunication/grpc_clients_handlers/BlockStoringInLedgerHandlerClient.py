import grpc
import logging

from comunication.grpc_protos import BlockStoringInLedger_pb2_grpc, BlockStoringInLedger_pb2


class BlockStoringInLedgerHandlerClient:
    """
    Handle the block storing in ledger communication part client side.

    After a client (a miner) win, he need to told it to other miners and after
    he must told to store the block!
    """

    def __init__(self):
        """
        Constructor with parameters
        """
        logging.basicConfig()

    @staticmethod
    def sendBlockStoringInLedgerNotification(time,
                                             seed,
                                             transactions_list,
                                             block_hash,
                                             lottery_number,
                                             miner_address,
                                             previous_block_hash,
                                             host):
        """
        Used by a miner to told to other miners that
        "he has winning mining game and they must storing block"

        :param time: Time in which block is mined
        :param seed: Seed used in proof of lottery
        :param transactions_list: List of transactions contained in the block
        :param block_hash: Hash of block
        :param lottery_number: Lottery number obtained by lottery(hash(block_hash))
        :param miner_address: Address of miner that mine block
        :param previous_block_hash: Hash of previous block
        :param host: Host to send message

        :return: If mining go well or not
        The verification is very easy:

            lottery(hash(miner_address)) = lottery(hash(block_hash)) = lottery_number,
                such that: block_hash = hash(transactions_list+seed)
        """

        # Establish a connection channel with the host (the miner) and get response
        with grpc.insecure_channel(host) as channel:
            client = BlockStoringInLedger_pb2_grpc.BlockStoringInLedgerStub(channel)

            # Send transaction request and wait response
            response = client.sendBlockStoringInLedgerNotification(
                BlockStoringInLedger_pb2.BlockStoringInLedgerRequest(time=time,
                                                                     seed=seed,
                                                                     transactions_list=transactions_list,
                                                                     block_hash=block_hash,
                                                                     lottery_number=lottery_number,
                                                                     miner_address=miner_address,
                                                                     previous_block_hash=previous_block_hash)
            )

        # If correct return true, false otherwise
        return response

