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

from matplotlib.pyplot import (
    plot, legend, figure, savefig, cla
)
import settings
from random import choice

NB_ITER = int(
    getattr(settings, 'EXECUTION_TIME', 2.0)
    / getattr(settings, 'TIME_SLOT', 0.005)
)
COLORS = ['black', 'red', 'blue', 'green', 'cyan']
DIR = 'graphs/'


def get_color(it):
    try:
        return it.next()
    except:
        return choice(COLORS)


def define_plot(x, data, color, label):
    plot(x, data, color=color, linewidth=1.0, linestyle='-', label=label)


def reset():
    cla()
    figure(figsize=(8, 6), dpi=80)


def define_from_dict(mydict):
    i = iter(COLORS)
    for k, v in mydict.iteritems():
        define_plot(
            range(len(v)), v,
            get_color(i), unicode(k)
        )
    legend(loc='upper right')


def graph_users_throughputs(users_th, algorithm_name):
    reset()
    define_from_dict(users_th)
    savefig(
        DIR + algorithm_name + u'_users_effective_throughputs.png'
    )


def graph_users_rbgs(users_rbgs, algorithm_name):
    reset()
    define_from_dict(users_rbgs)
    savefig(
        DIR + algorithm_name + u'_users_rbgs.png'
    )


def graph_users_th_throughputs(users_th, algorithm_name):
    reset()
    define_from_dict(users_th)
    savefig(
        DIR + algorithm_name + u'_users_theoritical_throughputs.png'
    )


def graph_users_cqis(users_cqis):
    reset()
    define_from_dict(users_cqis)
    savefig(DIR + 'users_cqis.png')
