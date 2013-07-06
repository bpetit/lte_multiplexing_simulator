

class Algorithm(object):
    """
    Defines the super class of each algorithms.
    Subclasses have to implement the following functions.
    """
    def __init__(self, *args, **kwargs):
        pass

    def choose_user(self, user_queues, last_user_imei, users_throughput):
        pass
