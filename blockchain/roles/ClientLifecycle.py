"""
Handle the lifecycle of a client
"""

# Utils modules
import sys
from datetime import datetime

# Transaction maker
from comunication.Transactions.TransactionHandlerClient import ClientTransactionHandler


def clientLifecycle(clientConfiguration, event, vote, address):
    """
    Lifecycle of a client

    :param clientConfiguration: Configuration to pass
    :param event: Event to vote
    :param vote: Vote to assign to event
    :param address: Address (address of blockchain NOT ip) of voter
    """

    # Get informations
    print(f"Run as a client...\n\nConfiruation:\n{clientConfiguration}\n")

    # Init client transaction handler
    clientTransactionHandler = ClientTransactionHandler()

    # Count the number of sending transactions
    sendingTransactionsCount = 0

    # Send transaction to miners (FOR EACH KNOWN HOST)
    for minerHostAddress in clientConfiguration.getKnownHosts():
        try:
            # Get current timestamp
            currentDateTime = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

            # Get response status (try to send transaction)
            responseStatus = clientTransactionHandler.sendTransaction(time=currentDateTime,
                                                                      event=event,
                                                                      vote=vote,
                                                                      address=address,
                                                                      host=minerHostAddress)

            # Transaction is going well (no errors or other stuffs) we update sending transaction counter
            if responseStatus:
                sendingTransactionsCount = sendingTransactionsCount + 1

        except Exception:
            print(f"Impossible to send transaction to {minerHostAddress}. Connection error. It is possible that you "
                  f"are not connected to "
                  f"network or your known host in {sys.argv[1]} is unreachable", file=sys.stderr)

    # Verify if transaction is sented to AT LEAST one host
    if sendingTransactionsCount > 0:
        print("Transaction sent in the network!")
        exit(0)

    # Impossible to sent transaction
    else:
        print(f"All known hosts in {sys.argv[1]} are unreachable!", file=sys.stderr)
