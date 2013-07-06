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

import Queue
# call settings with getattr(settings, 'PROPERTY_NAME', default_value)
import settings
from random import randint
from utils import StoppableThread, bits_constellation_generator
from time import time, sleep
from mapper import Mapper
from wx.lib.pubsub import Publisher
from wx import CallAfter


class Station(object):
    """
    A LTE base station. Receives data in a buffer and makes those
    datas accessible to the scheduler.
    """

    def __init__(self, *args, **kwargs):
        # let's define the user queues: a list of dictionaries composed
        # (for each user) of: an id, a cqa value, an average throughput value,
        # a maximum throughput value and a buffer of data
        self.user_queues = []
        self.users_throughput = {}
        self.users_th_throughput = {}
        self.users_cqis_hist = {}
        self.users_rbgs_hist = {}

    def connect_user_equipment(self, user_equipment):
        self.user_queues.append(
            [
                user_equipment.id,
                Queue.Queue(
                    maxsize=getattr(settings, 'USER_BUFFER_SIZE', '10')
                ),
                user_equipment.cqi
            ]
        )
        self.users_throughput[user_equipment.id] = []

    def record_throughput(self, user_id, throughput):
        """
        Adds a recorded throughput to a user list of throughputs.
        """
        if not user_id in self.users_throughput:
            self.users_throughput[user_id] = []
        self.users_throughput[user_id].append(throughput + 0.0)

    def record_th_throughput(self, user_id, throughput):
        if not user_id in self.users_th_throughput:
            self.users_th_throughput[user_id] = []
        self.users_th_throughput[user_id].append(throughput + 0.0)

    def get_average_throughput(self, user_id):
        """
        Returns the average value of throughput for a given user.
        If the user id given as parameter isn't known, returns None.
        """
        if not user_id in self.users_throughput:
            return None
        return sum(self.users_throughput[user_id]) / len(
            self.users_throughput[user_id])

    def add_incoming_packet(self):
        user_queue_index = randint(0, len(self.user_queues) - 1)
        user_queue = self.user_queues[user_queue_index]

        if not user_queue[1].full():
            user_queue[1].put(
                [
                    i for i in bits_constellation_generator(
                        getattr(settings, 'CONSTELLATION_SIZE', 4)
                    )
                ] * getattr(settings, 'NB_OFDM_SYMBOLS_PER_TIMESLOT', 7)
            )

    def report_cqi(self, user_equipment_id, cqi):
        try:
            # renew the CQI according to the one the UE has reported
            ue = next(i for i in self.user_queues if i[0] == user_equipment_id)
            ue[2] = cqi
            if not user_equipment_id in self.users_cqis_hist:
                self.users_cqis_hist[user_equipment_id] = []
            else:
                self.users_cqis_hist[user_equipment_id].append(cqi)
        except StopIteration:
            pass


class Scheduler(StoppableThread):
    """
    The scheduler class. may use differents algorithms.
    """

    def __init__(self, station):
        # selection of the algorithm to use
        self.algorithm = getattr(settings, 'SCHEDULER_ALGORITHM')()
        self.station = station
        self.current_user_imsi = None
        self.last_user_imsi = None
        self.start_time = None
        self.iteration_time = None
        self.mapper = Mapper()
        self.rbgs = None
        return super(Scheduler, self).__init__()

    def run(self):
        self.it = 0
        for u in self.station.user_queues:
            self.station.users_rbgs_hist[u[0]] = []
        timeslot = getattr(settings, 'TIME_SLOT', 0.005)
        nb_iter = (
            getattr(settings, 'EXECUTION_TIME', 2.0) /
            timeslot
        )
        while self.it < nb_iter and not self.stop_request:
            start_time = time()
            self.action()
            end_time = time()
            diff_time = end_time - start_time
            if diff_time < timeslot:
                sleep(timeslot - diff_time)
            self.it = self.it + 1
            CallAfter(Publisher().sendMessage, "refresh", '')

    def action(self):
        # IF YOU WISH TO IMPLEMENT AN ALGORITHM
        # YOU DON'T HAVE TO EDIT THIS FUNCTION
        self.rbgs = []

        for u in self.station.user_queues:
            self.station.users_rbgs_hist[u[0]].append(0)
        # sending datas to the mapper
        for i in range(getattr(settings, 'NB_RBG', 25)):
            data = []

            # call of the scheduling algo to choose the user to consider
            self.current_user_imsi = self.algorithm.choose_user(
                self.station.user_queues, self.last_user_imsi,
                self.station.users_throughput)
            # gets the user queue of the choosed user
            user_queue = next(
                i for i in self.station.user_queues
                if i[0] == self.current_user_imsi
            )
            for i in range(
                getattr(settings, 'NB_RB_PER_RBG')
                * getattr(settings, 'NB_OFDM_SYMBOLS_PER_TIMESLOT', 7)
            ):
                if not user_queue[1].empty():
                    # gets a constellation/data from this queue
                    data.append(user_queue[1].get())

            self.last_user_imsi = self.current_user_imsi

            self.rbgs.append((self.current_user_imsi, data))

            self.station.users_rbgs_hist[
                self.current_user_imsi][self.it] += 1

        # here we send the rbgs array to the mapper
        self.mapper.map_rbgs(self.rbgs)

        for u in self.station.user_queues:
            self.station.record_throughput(
                u[0], self.compute_used_throughput(
                    u[0],
                    [i for i in range(len(self.rbgs))
                     if self.rbgs[i][0] == u[0]]
                )
            )
            self.station.record_th_throughput(
                u[0],
                self.compute_th_throughput(
                    u[0],
                    [i for i in range(len(self.rbgs))
                     if self.rbgs[i][0] == u[0]]
                )
            )

        return super(Scheduler, self).action()

    def compute_used_throughput(self, user_id, rbgs_indexes):
        """
        Returns the throughput of the user in this timeslot
        considering the RBGs he's got and the infomations the
        can give.
        /!\ Return strange values /!\
        """
        timeslot = 0.0005
        data = 0
        tp = 0
        for i in rbgs_indexes:
            for rb in self.mapper.current_rbs:
                if rb.rbg_id == i and rb.data:
                    data += len(rb.data)
                    tp = (1 / timeslot) * data

        return tp

    def compute_th_throughput(self, user_id, rbgs_indexes):
        """
        Returns the theorical throughput which can be reached
        by the user during this timeslot.
        """
        timeslot = 0.0005
        size = getattr(settings, 'CONSTELLATION_SIZE', 4)
        size *= getattr(settings, 'NB_OFDM_SYMBOLS_PER_TIMESLOT', 7)
        size *= getattr(settings, 'SUB_CARRIER_PER_RB', 12)
        size *= getattr(settings, 'NB_RB_PER_RBG')
        th = (1 / timeslot) * len(rbgs_indexes) * size
        return th


class DataGenerator(StoppableThread):
    """
    Generates bits and adds those bits to the station queue.
    """
    def __init__(self, *args, **kwargs):
        self.station = kwargs.get('station')
        return super(DataGenerator, self).__init__()

    def action(self):
        sleep(getattr(settings, 'TIME_SLOT', 0.10) / 30)
        for i in range(len(self.station.user_queues)):
            self.station.add_incoming_packet()
        return super(DataGenerator, self).action()
