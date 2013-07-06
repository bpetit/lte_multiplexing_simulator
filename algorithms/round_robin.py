from algorithm import Algorithm


class RoundRobin(Algorithm):
    """
    """
    def __init__(self, *args, **kwargs):
        super(RoundRobin, self).__init__(args, kwargs)

    def choose_user(self, user_queues, last_user_imsi, users_throughput):
        if last_user_imsi:
        # if we have the last user imsi
            # we get the last user choosed thanks to its imei
            # last_user_imsi = next(u for u in user_queues
            # if u.id == last_user_imsi)
            last_user_index = user_queues.index(
                next(i for i in user_queues if i[0] == last_user_imsi)
            )
            # we return the next user whom index is last_user_id + 1 or 0
            next_user_index = last_user_index + 1 < len(user_queues) and \
                last_user_index + 1 or 0
            while user_queues[next_user_index][1].empty():
                next_user_index = next_user_index + 1 < len(user_queues) and \
                    next_user_index + 1 or 0
            next_user_imsi = user_queues[next_user_index][0]
        else:
        # if we haven't the last user imei we return
        # the first user of the list
            next_user_imsi = user_queues[0][0]
        return next_user_imsi
