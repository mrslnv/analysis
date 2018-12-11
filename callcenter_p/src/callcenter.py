import csv
import math
from collections import namedtuple

import simpy
from simpy.util import start_delayed

from timeutil import tu

Call = namedtuple("Call", ["time", "order"])


# adding ability to compute avg wait time
class CallCenter:
    def __init__(self, filename, qos=20):
        self.env = simpy.Environment()
        self.capacity = 1
        self.assistant = simpy.Container(self.env, 100, self.capacity)
        self.requestCount = 0
        self.waitAgg = 0
        self.count = 0
        self.qos = qos
        self.aboveQos = 0
        self.sim_data = []
        self.extraEvents = 0
        self.events = CallCenter.load_events(filename)
        self.regular_sche = None

        # schedule calls
        # move just before the first event (operator in service is the first event - before the first call)
        self.zeroTime = tu.time_sec("2015-12-14 00:00:00") - 1
        self.env.run(self.zeroTime)
        i = 0
        for evnt in self.events:
            i += 1
            start_delayed(self.env, self.accident(self.env, Call(evnt, i)), evnt - self.zeroTime)

    def assistent_leave(self):
        with self.assistant.get(1) as req:
            yield req
        self.capacity -= 1

    def assistent_join(self):
        with self.assistant.put(1) as req:
            yield req
        self.capacity += 1

    def accident(self, env, call):

        self.requestCount += 1

        start_time = env.now
        with self.assistant.get(1) as req:
            yield req
            self.got_to_operator(start_time, env, call)
            yield env.timeout(120)

        with self.assistant.put(1) as req:
            yield req

        self.requestCount -= 1

    def got_to_operator(self, start_time, env, call):
        w_time = env.now - start_time
        if start_time != call[0]:
            print("Bug, s_time:", start_time, " evnt time:", call[1], " envt i:", call[1])
        self.waitAgg += w_time
        if w_time > self.qos:
            self.aboveQos += 1

        self.count += 1

        self.sim_data.append([tu.time_str(start_time), w_time])

    def queue_len(self):
        return self.requestCount - self.capacity

    def get_avg_wait(self):
        return self.waitAgg / self.count

    def get_qos(self):
        return 100 * (1 - self.aboveQos / self.count)

    @staticmethod
    def load_events(filename):
        with open(filename, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skipp header
            data = list(reader)
        return [tu.time_sec(evnt[0]) for evnt in data]

    def write_stats(self, filename):
        with open(filename, "w", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(["time", "delay"])
            for w_time in self.sim_data:
                writer.writerow(w_time)

    @staticmethod
    def create_regular_schedule():
        regular_day_sche = [[1 for j in range(0, 24)] for i in range(0, 7)]
        for wd in range(0, 5):
            for h in range(8, 20):
                regular_day_sche[wd][h] += 1

        for wk in range(5, 7):
            for h in range(10, 20):
                regular_day_sche[wk][h] += 1
        return regular_day_sche

    def get_utilization(self):
        if self.regular_sche is None:
            raise Exception("Schedule must be loaded first with self.load_schedule(...)")

        stuff = 0
        for d in self.regular_sche:
            stuff += sum(d)
        stuff *= 77 # 77 weeks
        stuff += self.extraEvents * 24 # if extra events
        return len(self.events) / (30  * stuff)

    def load_schedule(self, regular_sche, extra_sche):
        # schedule personel shifts
        t = tu.time_sec("2015-12-14 00:00:00")
        prev = 0
        for i in range(77):
            for day in regular_sche:
                for h in day:
                    delta = h - prev
                    if delta > 0:
                        for j in range(delta):
                            start_delayed(self.env, self.assistent_join(), t - self.zeroTime)
                            prev += 1
                    if delta < 0:
                        for j in range(-delta):
                            start_delayed(self.env, self.assistent_leave(), t - self.zeroTime)
                            prev -= 1
                    t += 3600

        for e in extra_sche:
            t = tu.time_sec(e[0] + " 00:00:00")
            for i in range(e[1]):
                start_delayed(self.env, self.assistent_join(), t - self.zeroTime)
            t = tu.time_sec(e[0] + " 23:59:59")
            for i in range(e[1]):
                start_delayed(self.env, self.assistent_leave(), t - self.zeroTime)

        self.extraEvents = len(extra_sche)
        self.regular_sche = regular_sche

    def run_simulation(self):
        i = self.events[0] + 1
        print("Simulation starting")
        print("Start time:", tu.time_str(i))
        while True:
            self.env.run(until=i)
            next_evnt = self.env.peek()
            if next_evnt == math.inf:
                break
            i = next_evnt + 1
