"""
Handle the lifecycle of a client
"""

import sys
from datetime import datetime

from comunication.grpc_clients_handlers.TransactionHandlerClient import TransactionHandlerClient


def clientLifecycle(clientConfiguration, event, vote, address):
    """
    Lifecycle of a client

    :param clientConfiguration: Configuration to pass
    :param event: Event to vote
    :param vote: Vote to assign to event
    :param address: Address (address of blockchain NOT ip) of voter
    """

    # Get information
    print(f"Run as a client...\n\nConfiguration:\n{clientConfiguration}\n")

    # Count the number of sending transactions
    sendingTransactionsCount = 0

    # Send transaction to miners (FOR EACH KNOWN HOST)
    for minerHostAddress in clientConfiguration.getKnownHosts():
        try:
            # Get current timestamp
            currentDateTime = datetime.now().strftime("%d/%m/%Y,%H:%M:%S")

            # Get response status (try to send transaction)
            responseStatus = TransactionHandlerClient.sendTransaction(time=currentDateTime,
                                                                      event=event,
                                                                      vote=vote,
                                                                      address=address,
                                                                      host=minerHostAddress,
                                                                      broadcast=True)

            # Transaction is going well (no errors or other stuffs) we update sending transaction counter
            if responseStatus.valid:
                sendingTransactionsCount = sendingTransactionsCount + 1

        except Exception:
            print(f"Impossible to send transaction to {minerHostAddress}. Connection error. It is possible that you "
                  f"are not connected to "
                  f"network or your known host in {sys.argv[1]} is unreachable", file=sys.stderr)

    # Verify if transaction is sent to AT LEAST 1 host
    if sendingTransactionsCount >= 0:
        print("Transaction sent in the network!")
        exit(0)

    # Impossible to sent transaction
    else:
        print(f"All known hosts in {sys.argv[1]} are unreachable!", file=sys.stderr)
