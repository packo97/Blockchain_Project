import sys

# Handle configuration file
from configuration_handler.Config import Config

# Transaction maker
from comunication.TransactionHandler import ClientTransactionHandler, MinerTransactionHandler



def clientLifecicle(configuration):
    print(f"Run as a client...\n\nConfiruation:\n{configuration}\n")
    c = ClientTransactionHandler()
    try:
        print(c.sendTransaction(time="we", event="wee", vote="we", address="ouu"))

    except:
        print("Impossible to send transaction", file=sys.stderr)


def minerLifecicle(configuration):
    print(f"Run as a miner...\n\nConfiruation:\n{configuration}\n")
    s = MinerTransactionHandler()


if __name__ == '__main__':
    # Fetch configuration
    configuration = Config(configFilePath='config.json')

    # Run as a Client
    if configuration.getRole() == "client":
        clientLifecicle(configuration=configuration)

    # Run as a Miner
    elif configuration.getRole() == "miner":
        minerLifecicle(configuration=configuration)
