"""
View blockchain in realtime
"""
import os

from rich.console import Console
from rich.table import Table
from time import sleep

from ledger_handler.LedgerHandler import LedgerHandler


def blockchainViewerLifecycle(ledgerPath):
    """
    Print every time the blockchain ledger

    :param ledgerPath: Path of the ledger passed in configuration file
    """

    # Set Ledger Handler
    ledgerHandler = LedgerHandler(ledgerDatabasePath=ledgerPath)

    # Main loop
    while True:
        # Clear previous stuffs
        os.system("clear")

        # Create main table
        table = Table(title=f"Ledger: \"{ledgerPath}\" in realtime", show_lines=True)

        # Add headers
        table.add_column("Block Hash", justify="center", style="cyan")
        table.add_column("Seed", justify="center", style="green")
        table.add_column("Miner Address", justify="center", style="magenta")
        table.add_column("Lottery Number", justify="center", style="blue")
        table.add_column("Previous Block", justify="center", style="yellow")
        table.add_column("Timestamp", justify="center", style="white")
        table.add_column("Transactions", justify="center", style="red")

        # Fetch rows (blocks)
        allBlocks = ledgerHandler.viewBlocks()

        for row in allBlocks:
            # Block data
            hash = str(row[0])
            seed = str(row[1])
            minerAddress = str(row[2])
            lotteryNumber = str(row[3])
            previousHash = str(row[4])
            timestampBlock = str(row[5])

            # Transactions data
            transactions = ledgerHandler.viewAllTransactionsByBlocks(blockHash=hash)
            transactions = [f"{transaction[0]},{transaction[1]},{transaction[2]}" for transaction in transactions]

            # Make row with block and relative transactions
            table.add_row(hash,
                          seed,
                          minerAddress,
                          lotteryNumber,
                          previousHash,
                          timestampBlock,
                          "\n".join(transactions))

        # Print table
        console = Console()
        console.print(table)

        # Sleep 2 seconds
        sleep(3)

