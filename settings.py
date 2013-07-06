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

# default settings
from algorithms import round_robin, proportional_fair, max_cqi

# the class of the algorithm that the scheduler as to use
# don't suppress this one
SCHEDULER_ALGORITHM = round_robin.RoundRobin
#SCHEDULER_ALGORITHM = max_cqi.MaxCQI
#SCHEDULER_ALGORITHM = proportional_fair.ProportionalFair

RANDOM_CQI = True

# theoritical throughput per user
THEORITICAL_THROUGHPUT = 100.0

NB_TIMESLOTS_SIM = 15

# the number of client devices the software has to deal with
# at the beginning
NB_USERS = 4

# size of each user data buffer
USER_BUFFER_SIZE = 10

# time of exectution of the simulation in s
EXECUTION_TIME = 15.0

# nb of ressource blocks groups TODO: HAS TO BE COMPUTED
# WITH OTHER CARACTERISTICS ABOUT THE CHANNEL
NB_RBG = 25

# number of ofdm symbols per timeslot
NB_OFDM_SYMBOLS_PER_TIMESLOT = 7

# nb of bits per constellation
CONSTELLATION_SIZE = 4

# carrier specification (in kHz)
CARRIER_BANDWIDTH = 20000
SUB_CARRIER_SPACING = 15
SUB_CARRIER_PER_RB = 12

# frame specification (in ms)
FRAME = 2
SUB_FRAME = 0.4
TIME_SLOT = 0.2

# resource allocation specification
NB_RB = (CARRIER_BANDWIDTH / SUB_CARRIER_SPACING) / SUB_CARRIER_PER_RB
NB_RB_PER_RBG = NB_RB / NB_RBG
