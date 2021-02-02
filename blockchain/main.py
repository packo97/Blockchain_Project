import sys

# Handle configuration file
from configuration_handler.Config import Config

# Transaction maker
from comunication.Transactions.TransactionHandlerClient import ClientTransactionHandler
from comunication.Transactions.TransactionHandlerMiner import MinerTransactionHandler


def clientLifecycle(clientConfiguration):
    """
    Lifecycle of a client

    :param clientConfiguration: Configuration to pass
    """
    # Get informations
    print(f"Run as a client...\n\nConfiruation:\n{clientConfiguration}\n")

    # Init client transaction handler
    clientTransactionHandler = ClientTransactionHandler()

    # Send transaction
    try:
        print(clientTransactionHandler.sendTransaction(time="we", event="wee", vote="we", address="ouu"))

    except Exception:
        print("Impossible to send transaction", file=sys.stderr)


def minerLifecycle(minerConfiguration):
    """
    Lifecycle of a miner

    :param minerConfiguration: Configuration to pass
    """
    print(f"Run as a miner...\n\nConfiruation:\n{minerConfiguration}\n")
    s = MinerTransactionHandler()


if __name__ == '__main__':
    """
    Main method
    """
    # Fetch configuration
    configuration = Config(configFilePath='config.json')

    # Run as a Client
    if configuration.getRole == "client":
        clientLifecycle(clientConfiguration=configuration)

    # Run as a Miner
    if configuration.getRole == "miner":
        minerLifecycle(minerConfiguration=configuration)
