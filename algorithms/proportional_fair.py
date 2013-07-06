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
import settings


class ProportionalFair(Algorithm):

    def __init__(self, *args, **kwargs):
        super(ProportionalFair, self).__init__(args, kwargs)

    def choose_user(self, user_queues, last_user_imsi, users_throughput):
        best_metric_user_imsi = next(
            imsi for imsi, ths in users_throughput.items()
            if self.get_instant_throughput(ths) == max([
                self.get_instant_throughput(v) for k, v
                in users_throughput.items()
            ])
        )

        #user_queues[0][0]
        tmp_throughput = users_throughput.get(best_metric_user_imsi)
        best_metric = (
            self.get_instant_throughput(tmp_throughput)
            / (
                len(tmp_throughput) > 0 and
                (sum(tmp_throughput) / len(tmp_throughput))
                or getattr(settings, 'THEORITICAL_THROUGHPUT', 100.0)
            )
        )
        for u in user_queues:
            if not u[1].empty():
                throughputs = users_throughput.get(u[0])
                instant_throughput = self.get_instant_throughput(throughputs)
                average_throughput = (
                    len(throughputs) > 0 and
                    sum(throughputs) / len(throughputs)
                    or getattr(settings, 'THEORITICAL_THROUGHPUT', 100.0)
                )
                metric = instant_throughput / average_throughput
                if metric < best_metric:
                    best_metric_user_imsi = u[0]
                    best_metric = metric

        return best_metric_user_imsi

    def get_instant_throughput(self, throughputs):
        """
        Returns the last recorded throughput if there's any.
        Else returns the theoritical throughput.
        """
        if throughputs:
            return throughputs[-1]
        return getattr(settings, 'THEORITICAL_THROUGHPUT', 100.0)
