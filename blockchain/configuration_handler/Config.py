# Utils
import json
import sys


class Config:
    """Class that handle config.json file

    It contains all useful informations about startup configuration
    """

    def __init__(self, configFilePath):
        """Constructor with parameter

        Args:
            configFilePath (str): Path of configuration file to use
        """
        try:
            configFile = open(configFilePath)
            self.configData = json.load(configFile)

        except:
            print("Impossible to load config.json file", file=sys.stderr)

    def getKnownHosts(self):
        """Return all known hosts of a peer

        Returns:
            list: Known hosts
        """
        try:
            # A client MUST HAVE 3 known hosts AT LEAST
            if self.configData["role"] == "client" and len(self.configData["knownHosts"]) < 3:
                raise ValueError("A client must have AT LEAST 3 Known hosts")

            # A miner MUST HAVE 2 known hosts AT LEAST
            if self.configData["role"] == "miner" and len(self.configData["knownHosts"]) < 2:
                raise ValueError("A miner must have AT LEAST 2 Known hosts")

            return self.configData["knownHosts"]

        # In case there is known hosts but in wrong number
        except ValueError as valueError:
            print(valueError, file=sys.stderr)
            exit(1)

        # In case of error in find key
        except KeyError as keyError:
            print(
                "You must set a list of known hosts in config.json file\n\t3 hosts if you run as a client\n\t2 hosts if you run as a miner",
                file=sys.stderr)
            exit(1)

    def getRole(self):
        """Get role of user that run code.

        We can choose to run as a miner or as a client only
        changing config.json file

        Returns:
            str: Kind of user/role (miner or client)
        """
        try:
            if self.configData["role"] != "client" and self.configData["role"] != "miner":
                raise ValueError("Invalid role, you must set client or miner")

            return self.configData["role"]

        # If we add invalid role
        except ValueError as valueError:
            print(valueError, file=sys.stderr)
            exit(1)

        # In case of error in find key
        except KeyError as keyError:
            print(
                "You must set your role in config.json file to use our blockchain!\n\tminer if you want to mine with us\n\tclient if you want to be only a simple client",
                file=sys.stderr)
            exit(1)

    def getAddress(self):
        """Get address of user (client or miner)

        Returns:
            str: Address
        """
        try:
            return self.configData["address"]

        # In case of error in find key
        except:
            print("You must have an address to use our blockchain", file=sys.stderr)
            exit(1)

    def __str__(self):
        """Stringify content of config file
        """
        # Set all properties in a list
        properties = []
        properties.append(f"KNOWN_HOSTS: {self.getKnownHosts()}")
        properties.append(f"ROLE: {self.getRole()}")
        properties.append(f"ADDRESS: {self.getAddress()}")

        # Return all properties as a string (one property for every line)
        return "\n".join(properties)
