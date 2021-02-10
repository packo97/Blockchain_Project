import hashlib


class BlockMiningObject:

    def __init__(self,
                 time,
                 seed,
                 transactions_list,
                 block_hash,
                 lottery_number,
                 miner_address,
                 previous_block_hash):

        self.time = time
        self.seed = seed
        self.transactions_list = transactions_list
        self.block_hash = block_hash
        self.lottery_number = lottery_number
        self.miner_address = miner_address
        self.previous_block_hash = previous_block_hash
        self.hashedMinerAddress = hashlib.sha256(str.encode(self.miner_address)).hexdigest()

    def __str__(self):
        return f"({self.time},{self.seed},{self.transactions_list},{self.block_hash},{self.lottery_number},{self.miner_address},{self.previous_block_hash})"