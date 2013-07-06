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
# along with lte_multiplexing_simulator.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2013 Benoit Petit, Guillaume Mazoyer
#

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
