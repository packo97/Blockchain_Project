import sqlite3


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
        pass

    # ********** Useful operations for query blockchain (ex: view all transaction for a predefined event...) **********

    def read(self):
        pass
