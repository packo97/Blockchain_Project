class TransactionObject:
    """
    Class that handle a single transaction.

    Useful for order purpose,
    For example in Transaction handler we want use in operator
    or
    We want stringify it, ...
    """

    def __init__(self,
                 time,
                 address,
                 event,
                 vote):
        """
        Constructor with parameters

        :param time: Time in which transaction is sent
        :param address: Address of sender
        :param event: Event we have vote
        :param vote: Vote we take to event
        """

        # Init parameters
        self.time = time
        self.address = address
        self.event = event
        self.vote = vote

    def __str__(self):
        """
        Stringify a single transaction

        :return: String of transaction
        """

        return f"{self.time};{self.address};{self.event};{self.vote}|"

    def __eq__(self, other):
        """
        Equal operator, useful to verify double sending
        before mining

        :param other: Other instance of object

        :return: Objects are equal
        """
        return (self.address == other.address) and (self.event == other.event) and (self.vote == other.vote)
