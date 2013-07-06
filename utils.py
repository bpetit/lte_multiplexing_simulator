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

from threading import Thread
from random import randint


def generate_imsi():
    list = [randint(0, 9) for r in xrange(15)]
    return ''.join((str(i) for i in list))


def bits_constellation_generator(length):
    """
    Generator of random bits arrays of
    length = CONSTELLATION_SIZE setting.
    """
    for i in range(length):
        yield randint(0, 1)


class StoppableThread(Thread):
    """
    Subclass of Thread, defines common behavior
    of each Threaded class and gives a way to
    stop the Thread.
    """
    def __init__(self, *args, **kwargs):
        self.stop_request = False
        super(StoppableThread, self).__init__()

    def run(self):
        """
        Defines what the Thread does.
        """
        while not self.stop_request:
            self.action()

    def action(self):
        """
        Defines what the Thread does
        for each iteration.
        """
        pass

    def stop(self):
        """
        Requests the Thread to stop.
        """
        self.stop_request = True
