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
