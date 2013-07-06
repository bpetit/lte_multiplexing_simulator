from station import Station, DataGenerator, Scheduler
from user_equipment import UserEquipment
from mapper import FrameExtractor
from utils import generate_imsi
import settings
from gui import DrawPanel
from wx import App


def main():
    station = Station()
    gen = DataGenerator(station=station)
    sch = Scheduler(station=station)
    fex = FrameExtractor(channel=sch.mapper.channel)

    imsi_list = []
    user_equipments = []

    # generate a list of user equipments with unique ID
    for i in range(getattr(settings, 'NB_USERS', 5)):
        imsi = generate_imsi()
        if not imsi in imsi_list:
            imsi_list.append(imsi)
            user_equipments.append(UserEquipment(id=imsi))

    # connect all user equipments to the station
    for ue in user_equipments:
        station.connect_user_equipment(ue)
        ue.connect_to_station(station, fex)

    gen.start()
    sch.start()
    fex.start()

    for ue in user_equipments:
        ue.start()

    app = App()
    gui = DrawPanel(station, sch, user_equipments)
    gui.Show()
    app.MainLoop()

    sch.join()
    fex.stop()
    gen.stop()

    for ue in user_equipments:
        ue.stop()

    try:  # let's plot(graph) all this
        from plots import (
            graph_users_throughputs,
            graph_users_th_throughputs,
            graph_users_cqis,
            graph_users_rbgs
        )

        graph_users_throughputs(
            station.users_throughput,
            sch.algorithm.__class__.__name__
        )
        graph_users_th_throughputs(
            station.users_th_throughput,
            sch.algorithm.__class__.__name__
        )
        graph_users_cqis(station.users_cqis_hist)
        graph_users_rbgs(
            station.users_rbgs_hist,
            sch.algorithm.__class__.__name__
        )
    except ImportError:
        print "WARNING: matplotlib is not installed," \
            + "no plot will be generated"

if __name__ == '__main__':
    main()
