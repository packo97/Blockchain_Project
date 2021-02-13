import logging
import grpc

# Proto generated files
from comunication.grpc_protos import Transaction_pb2_grpc, Transaction_pb2


class TransactionHandlerClient:
    """
    Handle transaction by client view (client must only to send transactions)
    """

    def __init__(self):
        """
        Constructor without parameters
        """
        logging.basicConfig()

    @staticmethod
    def sendTransaction(time, address, event, vote, host, broadcast):
        """
        Sent transaction client side

        :param time: Sending time of transaction
        :param address: Of transaciton sender / voter
        :param event: Event to vote
        :param vote: Vote to assign to event
        :param host: Host/Miner ip to send transaction
        :param broadcast: If send transaction in broadcast or not

        :return: response
        """

        # Establish a connection channel with the host (the miner) and get response
        with grpc.insecure_channel(host) as channel:
            client = Transaction_pb2_grpc.TransactionStub(channel)

            # Send transaction request and wait response
            response = client.sendTransaction(
                Transaction_pb2.TransactionRequest(time=time,
                                                   address=address,
                                                   event=event,
                                                   vote=vote,
                                                   broadcast=broadcast)
            )

        # If correct return true, false otherwise
        return response
