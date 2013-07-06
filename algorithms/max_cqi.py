from algorithm import Algorithm


class MaxCQI(Algorithm):

    def __init__(self, *args, **kwargs):
        super(MaxCQI, self).__init__(args, kwargs)

    def choose_user(self, user_queues, last_user_imsi, users_throughput):
        # user equipments excluded for this selection
        excluded = []

        # get the first user with the max cqi
        candidate = self.get_user_equipment_with_max_cqi(user_queues, excluded)

        while user_queues[candidate][1].empty():
            # the user has nothing to send, select another one
            excluded.append(user_queues[candidate])
            candidate = self.get_user_equipment_with_max_cqi(user_queues, excluded)

        return user_queues[candidate][0]

    def get_user_equipment_with_max_cqi(self, users, excluded):
        max_cqi = users[0]

        for ue in users:
            if ue[2] >= max_cqi[2] and not ue in excluded:
                max_cqi = ue

        return users.index(max_cqi)
