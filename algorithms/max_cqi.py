# This file is part of lte_multiplexing_simulator.
#
# lte_multiplexing_simulator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# lte_multiplexing_simulator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2013 Benoit Petit, Guillaume Mazoyer
#

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
