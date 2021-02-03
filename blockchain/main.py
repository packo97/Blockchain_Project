# Utils modules
import sys
import re

# Handle json configuration file
from comunication.transactions.validation.TransactionValidator import isTransactionValid
from configuration_handler.Config import Config

# Lifecycles
from roles.ClientLifecycle import clientLifecycle
from roles.MinerLifecycle import minerLifecycle


if __name__ == '__main__':
    """
    Main method
    """

    # Run main.py configuration_file_path.json ...eventual other_args...
    # eventual other_args for client are event vote
    if len(sys.argv) >= 2:

        # Fetch configuration
        configFilePath = sys.argv[1]
        configuration = Config(configFilePath=configFilePath)

        # Run as a Client
        if configuration.getRole == "client":
            # A client must sent a vote with a valid vote and valid event
            try:
                # Validate transaction with regex
                event = sys.argv[2]
                vote = sys.argv[3]
                validFormatVote = isTransactionValid(event=event, vote=vote)

                # If transaction is in a valid format event vote
                if validFormatVote[0] and validFormatVote[1]:
                    transactionContent = f"{event};{vote}"
                    clientLifecycle(clientConfiguration=configuration,
                                    event=event,
                                    vote=vote,
                                    address=configuration.getAddress())

            # Not add event and vote in arguments
            except IndexError as indexError:
                print("You must pass vote and event to vote as a client.\n\tpython main.py "
                      "configuration_file_path.json event vote\n"
                      "(NOTE: order is important FIRST event, SECOND vote)", file=sys.stderr)

        # Run as a Miner
        if configuration.getRole == "miner":
            minerLifecycle(minerConfiguration=configuration)

    # Otherwise (we need a configuration file)
    else:
        print("You need to use a configuration json file to run application", file=sys.stderr)
