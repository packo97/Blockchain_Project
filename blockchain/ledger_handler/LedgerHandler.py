import sqlite3

from mining.mining_utils.ProofOfLottery import ProofOfLottery


class LedgerHandler:
    """
    class that handle ledger database
    """

    def __init__(self, ledgerDatabasePath):
        """
        Constructor with parameters

        :param ledgerDatabasePath: Path of sqlite3 database to use to store our blockchain
        """

        # Init connection and cursor for sqlite
        self.connection = sqlite3.connect(ledgerDatabasePath)
        self.databaseCursor = self.connection.cursor()

    def __del__(self):
        """
        Destructor, it close db connection on instance destruction of this class
        """
        self.connection.close()

    # ********** Useful operations for miner **********

    def getAllEventVotedByAnAddress(self, event, address):
        """
        Return all events that are voted by an address.

        It is useful for VALIDATION OF TRANSACTION.

        IN FACT MUST BE IMPOSSIBLE that the same address can vote
        twice for the same event"

        :param event: Event to vote
        :param address: Address of voter

        :return: Result of query

        NOTE: result is iterable object:
            for r in result:
                print(r)
        """
        result = self.databaseCursor.execute(f'SELECT event '
                                             f'FROM "Transaction" '
                                             f'WHERE address="{address}" '
                                             f'AND '
                                             f'event="{event}"')
        return result

    def getPreviousBlockHash(self):
        """
        Get the hash of last block.

        It is useful because miner must send previous hash in the block

        :return: Previous hash of block
        """
        result = self.databaseCursor.execute("SELECT hash FROM Block ORDER BY block_id DESC LIMIT 1")

        return result

    def insertBlockInLedger(self, block):
        """
        Insert a block in blockchain

        :param block: Block to add in ledger

        """

        # De stringify block hash
        transactionObjectsList = ProofOfLottery.deStringifyTransactionString(block.transactionsList)

        # Get previous block hash
        block.previousBlockHash = self.getPreviousBlockHash().fetchone()[0]

        #  Query for add block
        addBlockQuery = f"INSERT INTO Block(hash, seed, miner_address, lottery_number, previous_hash, timestamp_block) "\
                f"VALUES ('{block.blockHash}',"\
                f"{block.seed},"\
                f"'{block.minerAddress}',"\
                f"'{block.lotteryNumber}',"\
                f"'{block.previousBlockHash}',"\
                f"'{block.time}')"

        self.databaseCursor.execute(addBlockQuery)

        # Query for add transactions
        for transaction in transactionObjectsList:
            addTransactionQuery = f"INSERT INTO 'Transaction' (timestamp_transaction, event, vote, address, block_hash) "\
                                  f"VALUES ('{transaction.time}', '{transaction.event}', " \
                                  f"{transaction.vote}, " \
                                  f"'{transaction.address}', " \
                                  f"'{block.blockHash}')"

            self.databaseCursor.execute(addTransactionQuery)

        # Final commit
        self.connection.commit()

    # ********** Useful operations for query blockchain (ex: view all transaction for a predefined event...) **********

    def read(self):
        pass
