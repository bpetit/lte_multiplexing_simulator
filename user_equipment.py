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

import settings
from random import randint
from time import sleep
from utils import StoppableThread


class UserEquipment(StoppableThread):
    """
    A LTE user equipment. Receives data in a buffer.
    """

    def __init__(self, *args, **kwargs):
        self.id  = kwargs.get('id')
        self.station = None
        self.frame_extractor = None
        self.cqi = None
        self.cqi = self.generate_cqi()
        self.instant_throughput = 0
        self.average_throughput = 0
        self.data = []
        return super(UserEquipment, self).__init__()

    def get_resources_blocks(self):
        return self.frame_extractor.get_resources_blocks_for(self.id)

    def receive_incoming_data(self, resources_block):
        # get the data of the resources block
        self.data.extend(resources_block.data)

    def connect_to_station(self, station, frame_extractor):
        self.station = station
        self.frame_extractor = frame_extractor

    def generate_cqi(self):
        if self.cqi is None or getattr(settings, 'RANDOM_CQI', False):
            return randint(0, 15)
        else:
            return self.cqi

    def action(self):
        # need to be tweaked
        sleep(getattr(settings, 'TIME_SLOT', 0.10)/4 * (getattr(settings,
            'FRAME') / getattr(settings, 'TIME_SLOT')))

        # generate a new CQI and report it
        self.cqi = self.generate_cqi()
        if self.station:
            self.station.report_cqi(self.id, self.cqi)

        # get all resources blocks
        resources_blocks = self.get_resources_blocks()

        # no resources blocks available
        if not resources_blocks or resources_blocks.empty():
            return

        # receive data from resources blocks
        while not resources_blocks.empty():
            self.receive_incoming_data(resources_blocks.get())

        return super(UserEquipment, self).action()
