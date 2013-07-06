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
