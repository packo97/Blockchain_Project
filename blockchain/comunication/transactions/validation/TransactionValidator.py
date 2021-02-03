
def isTransactionValid(event, vote):
    """
    Validate format of transactions
    :param event: Event to vote
    :param vote: Vote assign to event
    :return: event is not null and vote is numeric
    """
    return len(event) > 0, vote.isnumeric()