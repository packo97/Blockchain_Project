import sqlite3


class LedgerHandler:
    """
    class that handle ledger database
    """

    def __init__(self, ledgerDatabasePath):
        self.connection = sqlite3.connect(ledgerDatabasePath)
        self.databaseCursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    # useful operations for miner
    def getAllEventVotedByAnAddress(self, event, address):
        result = self.databaseCursor.execute(f'SELECT event FROM "Transaction" WHERE address="{address}" AND event="{event}"')
        for r in result:
            print(r)



    # useful operations for query blockchain (ex: view all transaction for a predefined event...)
    def read(self):
        pass
