import sys

from configuration_handler.Config import Config
from roles.BlockchainViewerLifecycle import blockchainViewerLifecycle

if __name__ == '__main__':
    """
    Main method
    """

    # Run ledgerViewer.py configuration_file_path.json
    if len(sys.argv) >= 2:

        # Fetch configuration
        configFilePath = sys.argv[1]
        configuration = Config(configFilePath=configFilePath)

        # Run as viewer lifecycle
        blockchainViewerLifecycle(ledgerPath=configuration.getLedgerDatabasePath())

    # Otherwise (we need a configuration file)
    else:
        print("You need to use a configuration json file to run application", file=sys.stderr)
