from algorithm import Algorithm
import settings


class ProportionalFair(Algorithm):

    def __init__(self, *args, **kwargs):
        super(ProportionalFair, self).__init__(args, kwargs)

    def choose_user(self, user_queues, last_user_imsi, users_throughput):
        best_metric_user_imsi = next(
            imsi for imsi, ths in users_throughput.items()
            if self.get_instant_throughput(ths) == max([
                self.get_instant_throughput(v) for k, v
                in users_throughput.items()
            ])
        )

        #user_queues[0][0]
        tmp_throughput = users_throughput.get(best_metric_user_imsi)
        best_metric = (
            self.get_instant_throughput(tmp_throughput)
            / (
                len(tmp_throughput) > 0 and
                (sum(tmp_throughput) / len(tmp_throughput))
                or getattr(settings, 'THEORITICAL_THROUGHPUT', 100.0)
            )
        )
        for u in user_queues:
            if not u[1].empty():
                throughputs = users_throughput.get(u[0])
                instant_throughput = self.get_instant_throughput(throughputs)
                average_throughput = (
                    len(throughputs) > 0 and
                    sum(throughputs) / len(throughputs)
                    or getattr(settings, 'THEORITICAL_THROUGHPUT', 100.0)
                )
                metric = instant_throughput / average_throughput
                if metric < best_metric:
                    best_metric_user_imsi = u[0]
                    best_metric = metric

        return best_metric_user_imsi

    def get_instant_throughput(self, throughputs):
        """
        Returns the last recorded throughput if there's any.
        Else returns the theoritical throughput.
        """
        if throughputs:
            return throughputs[-1]
        return getattr(settings, 'THEORITICAL_THROUGHPUT', 100.0)
