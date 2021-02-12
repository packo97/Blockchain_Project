import hashlib


class BlockMiningObject:
    """
    Block mining object.

    It is useful for for sorting and string conversion
    """

    def __init__(self,
                 time,
                 seed,
                 transactionsList,
                 blockHash,
                 lotteryNumber,
                 minerAddress,
                 previousBlockHash):
        """
        Constructor with parameters

        :param time: Time in which block mining request is sent
        :param seed: Seed of block mining request
        :param transactionsList: Transactions list of block mining request
        :param blockHash: Block hash of block mining request
        :param lotteryNumber: Lottery number of block mining request
        :param minerAddress: Miner address of block mining request
        :param previousBlockHash: Previous block hash of block mining request
        """

        self.time = time
        self.seed = seed
        self.transactionsList = transactionsList
        self.blockHash = blockHash
        self.lotteryNumber = lotteryNumber
        self.minerAddress = minerAddress
        self.previousBlockHash = previousBlockHash

        # Useful for verification. We make the hash to avoid that a miner can create a "cheat hash"
        self.hashedMinerAddress = hashlib.sha256(str.encode(self.minerAddress)).hexdigest()

    def __str__(self):
        """
        Convert to string

        :return: Stringify version of block mining object
        """
        return f"({self.minerAddress},{self.seed},{self.transactionsList})"
        # return f"({self.time},{self.seed},{self.transactionsList},{self.blockHash}," \
        #        f"{self.lotteryNumber},{self.minerAddress},{self.previousBlockHash})"

    def __eq__(self, other):
        """
        Equal operator to define if two block mining request are equal
        It is useful in storing part

        :param other: Other block mining object

        :return: If block mining objects are equal
        """
        return \
            self.time == other.time and \
            self.seed == other.seed and \
            self.transactionsList == other.transactionsList and \
            self.blockHash == other.blockHash and \
            self.lotteryNumber == other.lotteryNumber and \
            self.minerAddress == other.minerAddress and \
            self.previousBlockHash == other.previousBlockHash
