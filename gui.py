from random import randint
import wx
import settings


NB_RB = getattr(settings, 'NB_RB', 100)
FRAME_WIDTH = getattr(settings, 'FRAME_WIDTH', 1024)
FRAME_HEIGHT = getattr(settings, 'FRAME_HEIGHT', 768)
CHANNEL_X_PERCENT = getattr(settings, 'CHANNEL_X_PERCENT', 30)
CHANNEL_Y_PERCENT = getattr(settings, 'CHANNEL_Y_PERCENT', 5)
RB_HEIGHT = getattr(
    settings, 'RB_HEIGHT', ((100 - CHANNEL_Y_PERCENT * 1) * FRAME_HEIGHT / 100)
    / NB_RB
)
RB_WIDTH = getattr(
    settings, 'RB_WIDTH', ((100 - CHANNEL_X_PERCENT * 1) * FRAME_WIDTH / 100)
    / NB_RB
)
NB_RBG = getattr(settings, 'NB_RBG', 25)
RBG_HEIGHT = getattr(
    settings, 'RBG_HEIGHT', (80 * FRAME_HEIGHT / 100) / NB_RBG
)
RBG_WIDTH = getattr(settings, 'RBG_WIDTH', RBG_HEIGHT)
USERS_COLORS = {}
TIMER_LAPS = getattr(settings, 'TIMER_LAPS', 1)
X_ORIGIN = getattr(
    settings, 'X_ORIGIN', FRAME_WIDTH * CHANNEL_X_PERCENT / 100
)
Y_ORIGIN = getattr(
    settings, 'Y_ORIGIN', FRAME_HEIGHT * CHANNEL_Y_PERCENT / 100
)
USERS_QUEUES_X_PERCENT = getattr(
    settings, 'USERS_QUEUES_X_PERCENT', 8
)
USERS_QUEUES_Y_PERCENT = getattr(
    settings, 'USERS_QUEUES_Y_PERCENT', 15
)


class DrawPanel(wx.Frame):
    """
    Draws users queues, buffered rbgs, channel
    and user equipements. Refreshes itself each
    TIMER_LAPS duration.
    """

    def __init__(self, station,  sch, ues):
        wx.Frame.__init__(
            self, None, title="[RE56] LTE multiplexing simulator",
            size=(FRAME_WIDTH, FRAME_HEIGHT)
        )
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        #self.timer = wx.Timer(self, 1)
        #self.timer.Start(2, oneShot=False)
        #self.Bind(wx.EVT_TIMER, self.OnPaint)
        self.dc = None
        self.channel_drawn = False
        self.ues_drawn = False
        self.station = station
        self.sch = sch
        self.ues = ues
        self.__init_ue_colors()
        self.SetBackgroundColour(wx.WHITE)
        wx.lib.pubsub.Publisher().subscribe(self.OnPaint, "refresh")
        wx.lib.pubsub.Publisher().subscribe(self.__clear_free_timeslots,
                                            "tsupdate")

    def __init_ue_colors(self):
        colors = [
            wx.BLACK, wx.RED, wx.BLUE,
            wx.GREEN, wx.CYAN, wx.LIGHT_GREY
        ]
        i = iter(colors)
        for u in self.ues:
            try:
                USERS_COLORS[u.id] = i.next()
            except StopIteration:
                r = randint(0, 255)
                g = randint(0, 255)
                b = randint(0, 255)
                USERS_COLORS[u.id] = (r, g, b)

    def OnPaint(self, event=None):
        if not self.dc:
            self.dc = wx.PaintDC(self)
        if not self.ues_drawn:
            self.__draw_ues()
        #if not self.channel_drawn:
        #    self.draw_channel()
        self.__draw_user_queues()
        self.__color_rbgs()
        self.__color_rbs()
        self.__draw_throughputs()
        #self.__clear_free_timeslots(10, 20)
        #self.timer.Start(TIMER_LAPS)

    def __draw_ues(self):
        self.dc.DrawText(
            u'UEs / IMSI',
            925, 50
        )
        self.dc.SetPen(wx.Pen(wx.BLACK, 1))
        for i in range(len(self.ues)):
            self.__color_rectangle(
                FRAME_WIDTH - 100,
                0 + FRAME_HEIGHT * 20 / 100 + (i - 1) * 80 + 20,
                USERS_COLORS[self.ues[i].id],
                40, 60, True
            )
            self.dc.DrawText(
                str(self.ues[i].id),
                FRAME_WIDTH - 120,
                (FRAME_HEIGHT * 20 / 100 + (i - 1) * 80 - 3) + 5
            )
        self.ues_drawn = True

    def __draw_throughputs(self):
        self.dc.DrawText(
            u'Throughputs',
            760, 50
        )
        for i in range(len(self.ues)):
            x = FRAME_WIDTH - 300
            y = 0 + FRAME_HEIGHT * 20 / 100 + (i - 1) * 80 + 20
            self.__color_rectangle(
                x, y, wx.WHITE, 200, 20
            )
            try:
                self.dc.DrawText(
                    unicode(
                        self.station.users_throughput[self.ues[i].id][-1] / 1000
                    ) + 'kbps / ' +
                    unicode(self.station.users_th_throughput[self.ues[i].id][-1]
                            / 1000000) +
                    'Mbps',
                    x, y
                )
            except IndexError:
                pass

    def draw_channel(self):
        dc = self.dc
        dc.Clear()
        dc.SetPen(wx.Pen(wx.WHITE, 1))
        dc.SetBrush(wx.Brush(wx.WHITE))
        for i in range(len(self.sch.mapper.channel[0])):
            for j in range(len(self.sch.mapper.channel)):
                dc.DrawRectangle(
                    X_ORIGIN + (i - 1) * RB_WIDTH,
                    Y_ORIGIN + (j - 1) * RB_HEIGHT,
                    RB_WIDTH,
                    RB_HEIGHT
                )
        if not self.channel_drawn:
            self.channel_drawn = True

    def __clear_free_timeslots(self, msg):
        start = msg.data[0]
        end = msg.data[1]
        self.dc.SetPen(wx.Pen(wx.WHITE, 1))
        self.dc.SetBrush(wx.Brush(wx.BLACK))
        self.__color_rectangle(
            X_ORIGIN + (start - 1) * RB_WIDTH,
            Y_ORIGIN - RB_HEIGHT, wx.WHITE,
            (end - (start - 1)) * RB_WIDTH,
            NB_RB * RB_HEIGHT
        )

    def __color_rbs(self):
        self.dc.DrawText(
            u'Channel / RBs', X_ORIGIN + 100,
            10
        )
        for j in range(len(self.sch.mapper.channel)):
            for i in range(len(self.sch.mapper.channel[j])):
                try:
                    if self.sch.mapper.channel[j][i].user_id \
                            and self.sch.mapper.channel[j][i].data:
                        self.__color_cell(
                            X_ORIGIN + (i - 1) * RB_WIDTH,
                            Y_ORIGIN + (j - 1) * RB_HEIGHT,
                            USERS_COLORS[self.sch.mapper.channel[j][i].user_id]
                        )
                    else:
                        self.__color_empty_cell(
                            X_ORIGIN + (i - 1) * RB_WIDTH,
                            Y_ORIGIN + (j - 1) * RB_HEIGHT
                        )
                except IndexError:
                    pass
                except KeyError:
                    pass

    def __color_rbgs(self):
        self.dc.DrawText(
            u'RBG',
            X_ORIGIN - 100, 25
        )
        if self.sch.rbgs:
            for i in range(len(self.sch.rbgs)):
                try:
                    self.__color_rbg(
                        X_ORIGIN - 100,
                        Y_ORIGIN + 50 + (i - 1) * RBG_HEIGHT,
                        USERS_COLORS[self.sch.rbgs[i][0]]
                    )
                except IndexError:
                    pass

    def __color_rectangle(self, x, y, color, width=RB_WIDTH, height=RB_HEIGHT,
                          borders=False):
        if not borders:
            self.dc.SetPen(wx.Pen(color))
        else:
            self.dc.SetPen(wx.Pen('#EEEEEE', 1))
        self.dc.SetBrush(wx.Brush(color))
        self.dc.DrawRectangle(
            x, y, width, height
        )

    def __color_empty_cell(self, x, y):
        self.__color_cell(x, y, '#ffffff', False)

    def __color_cell(self, x, y, color, borders=True):
        self.__color_rectangle(x, y, color, RB_WIDTH, RB_HEIGHT, borders)

    def __color_rbg(self, x, y, color):
        self.__color_rectangle(x, y, color, RBG_WIDTH, RBG_HEIGHT, True)

    def __draw_user_queues(self):
        x = FRAME_WIDTH * USERS_QUEUES_X_PERCENT / 100
        y = FRAME_WIDTH * USERS_QUEUES_Y_PERCENT / 100
        self.dc.DrawText(u'Users queues', x + 5, y - 50)
        for i in range(len(self.station.user_queues)):
            self.__color_rectangle(
                0, y + (i - 1) * 20,
                wx.WHITE, 60, 20
            )
            self.dc.DrawText(
                u'CQI = ' + unicode(self.station.user_queues[i][2]),
                0, y + (i - 1) * 20
            )
            for j in range(self.station.user_queues[i][1].qsize()):
                self.__color_rectangle(
                    x + (j - 1) * 10,
                    y + (i - 1) * 20,
                    USERS_COLORS[self.station.user_queues[i][0]],
                    10, 10, True
                )
