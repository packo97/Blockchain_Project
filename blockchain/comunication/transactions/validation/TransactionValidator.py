
class TransactionValidator:
    """
    Verity transaction format
    """

    @staticmethod
    def isTransactionFormatValid(event, vote):
        """
        Validate sintattic format of transactions

        :param event: Event to vote
        :param vote: Vote assign to event
        :return: event is not null and vote is numeric
        """
        return (len(event) > 0) and ('|' not in event), vote.isnumeric()
