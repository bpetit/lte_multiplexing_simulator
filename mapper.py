import Queue
import settings
from time import sleep
from utils import StoppableThread
from wx.lib.pubsub import Publisher
from wx import CallAfter


class Mapper(object):
    """
    Makes the relation between RBGs and
    ressources blocks.
    """
    def __init__(self):
        self.channel = [
            [] for i in range(getattr(settings, 'NB_RB'))
        ]
        self.cyclic_mapping = getattr(settings, 'CYCLIC_MAPPING', False)
        if self.cyclic_mapping:
            self.rb_to_rbgs = {
                k: v for (k, v) in range(getattr(settings, 'NB_RB'), None)
            }

    def __new_rbs(self):
        if not self.cyclic_mapping:
            self.current_rbs = [
                ResourceBlock(
                    (i * getattr(settings, 'NB_RBG'))
                    / getattr(settings, 'NB_RB')
                )
                for i in range(getattr(settings, 'NB_RB'))
            ]
        #else:
        #    for rb_id in range(getattr(settings, 'NB-RB')):
        #        previous_rbg_id = self.rb_to_rbgs[rb_id]
        #        if previsou_rbg_id is not None:
        #            rbg_id = previous_rbg_id + 1 < getattr(settings, 'NB_RBG') - 1\
        #                and previsou_rbg_id + 1 or 0
        #        else:
        #            pass
        #            #rbg_id = (rb_id * )
        #        rbg_id = previous_rbg_id is not None and \
        #            previous_rbg_id + 1
        #        self.current_rbs.append(
        #            ResourceBlock(
#
#                    )
#                )

    def __send_rbs(self):
        for rb in self.channel:
            rb.insert(0, self.current_rbs[self.channel.index(rb)])

    def map_rbgs(self, rbgs):
        self.__new_rbs()
        self.rbgs = rbgs
        for rbg in self.rbgs:
            for rb in self.current_rbs:
                if rb.rbg_id == self.rbgs.index(rbg):
                    rb.user_id = rbg[0]
                    if len(rbg[1]) > 0:
                        data = rbg[1][0]
                        rb.put_data(data)
                        rbg[1].remove(data)
        self.__send_rbs()


class ResourceBlock(object):
    """
    A piece of frequency allocable to a user.
    Has a size in frequency which is traditionally
    180 Khz in frequency and 0.5ms in time (this value
    is replaced by the one choosed as the setting
    TIME_SLOT)
    """
    def __init__(self, rbg_id):
        self.rbg_id = rbg_id
        self.user_id = None
        self.data = None

    def put_data(self, data):
        size = (
            getattr(settings, 'CONSTELLATION_SIZE', 4)
            * getattr(settings, 'NB_OFDM_SYMBOLS_PER_TIMESLOT', 7)
            * getattr(settings, 'SUB_CARRIER_PER_RB', 12)
        )
        if len(data) <= size:
            self.data = data
        else:
            self.data = data[0: (size - 1)]

    def __unicode__(self):
        return "RBG: " + str(self.rbg_id) \
            + " USER: " + str(self.user_id) \
            + " DATA: " + str(self.data)


class FrameExtractor(StoppableThread):
    """
    A process that will compose a frame.
    """
    def __init__(self, *args, **kwargs):
        self.channel = kwargs.get('channel')
        self.frames = []
        self.per_user = {}
        return super(FrameExtractor, self).__init__()

    def get_resources_blocks_for(self, user_equipment):
        try:
            return self.per_user[user_equipment]
        except KeyError:
            return None

    def parse_frame(self, frame):
        for rb in frame:
            # no data in the resources blocks, ignore it
            if not rb.data:
                continue

            if rb.user_id not in self.per_user:
                # we did not have any data for the current user yet
                self.per_user[rb.user_id] = Queue.Queue()

            # add resources blocks to the user queue
            self.per_user[rb.user_id].put(rb)

    def action(self):
        # need to be tweaked
        sleep(getattr(settings, 'TIME_SLOT', 0.10))
        frame_length = 20
        #getattr(settings, 'FRAME') / getattr(settings,
                #'TIME_SLOT')

        # can't compose a frame
        if len(self.channel[0]) <= 1:
            return

        for rb in self.channel:
            frame = []

            # check that we have enough timeslots to compose a frame
            if len(rb) >= int(frame_length):
                index = len(rb) - 1

                # compose a frame based on the number of timeslots needed
                # each frame is composed for each resources block
                # remove the timeslot from the rb/channel once we retrieved it
                for i in range(int(frame_length)):
                    timeslot = rb[len(rb) - 1]
                    frame.append(timeslot)
                    rb.remove(timeslot)

                # register the frame
                self.parse_frame(frame)
                self.frames.append(frame)

                # notify the UI
                CallAfter(
                    Publisher().sendMessage, "tsupdate",
                    (index - int(frame_length), index)
                )

        return super(FrameExtractor, self).action()
