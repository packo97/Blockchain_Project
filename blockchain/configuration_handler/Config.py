# Utils
import json
import sys


class Config:
    """
    Class that handle configForClient.json file

    It contains all useful information about startup configuration
    """

    def __init__(self, configFilePath):
        """
        Constructor with parameters

        :param configFilePath: Path of configuration file to use
        """
        # Try to open configuration file
        try:
            configFile = open(configFilePath)
            self.configData = json.load(configFile)

        # Impossible to open file (it doesn't exists)
        except Exception:
            print(f"Error on load {self.configFilePath} file", file=sys.stderr)

    def getKnownHosts(self):
        """
        Get the list of all known hosts

        :return: Known hosts
        """
        try:
            # IMPORTANT: A client MUST HAVE 3 known hosts AT LEAST
            if self.configData["role"] == "client" and len(self.configData["knownHosts"]) < 3:
                raise ValueError("A client must have AT LEAST 3 Known hosts")

            # IMPORTANT: A miner MUST HAVE 2 known hosts AT LEAST
            if self.configData["role"] == "miner" and len(self.configData["knownHosts"]) < 2:
                raise ValueError("A miner must have AT LEAST 2 Known hosts")

            return self.configData["knownHosts"]

        # In case there are known hosts BUT in wrong number (SEE above rules)
        except ValueError as valueError:
            print(valueError, file=sys.stderr)
            exit(1)

        # In case of error in find key in json file
        except KeyError as keyError:
            print(
                "You must set a list of known hosts in configForClient.json file\n\t3 hosts if you run as a client\n\t2 hosts "
                "if you run as a miner",
                file=sys.stderr)
            exit(1)

    @property
    def getRole(self):
        """
        Get current user role (miner or client)

        We can choose to run as a miner or as a client only
        changing configForClient.json file

        :return: Kind of user/role (miner or client)
        """
        try:
            # Allowed roles must be ONLY client and miner
            if self.configData["role"] != "client" and self.configData["role"] != "miner":
                raise ValueError("Invalid role, you must set client or miner")

            return self.configData["role"]

        # Invalid role inserted in role key
        except ValueError as valueError:
            print(valueError, file=sys.stderr)
            exit(1)

        # In case of error in find role key in json file
        except KeyError as keyError:
            print(
                "You must set your role in configForClient.json file to use our blockchain!\n\tminer if you want to mine with "
                "us\n\tclient if you want to be only a simple client",
                file=sys.stderr)
            exit(1)

    def getAddress(self):
        """
        Get address of peer (both for miner and client)
        :return: Address of peer
        """
        try:
            return self.configData["address"]

        # In case of error in find address key in json file
        except Exception:
            print("You must have an address to use our blockchain. Set it on your configuration json file in field "
                  "address", file=sys.stderr)
            exit(1)

    def getMinerPort(self):
        """
        Return the port that we used for running the miner

        :return: The port of miner
        """
        try:
            return self.configData["minerPort"]

        # In case of error in find address key in json file
        except Exception:
            print("You must running a miner with a port, add minerPort field in configuration json file",
                  file=sys.stderr)
            exit(1)

    def getLedgerDatabasePath(self):
        """
        Return the path of sqlite3 ledger db

        :return: The path of sqlite3 ledger db
        """
        try:
            return self.configData["ledgerDatabasePath"]

        # In case of error in find address key in json file
        except Exception:
            print("You must running a miner with a ledger file",
                  file=sys.stderr)
            exit(1)

    def __str__(self):
        """
        Stringify content of config file
        :return: String of all options/keys of json file
        """

        # Set all properties in a list
        properties = [f"KNOWN_HOSTS: {self.getKnownHosts()}",
                      f"ROLE: {self.getRole}",
                      f"ADDRESS: {self.getAddress()}"]

        # Return all properties as a string (one property for every line)
        return "\n".join(properties)
