import simpy
from simpy.util import start_delayed
from collections import namedtuple
from simulation.timeutil import tu

Call = namedtuple("Call", ["time", "order"])


class CallCenter:
    def __init__(self, env, events, capacity=2):
        self.CAPACITY = capacity
        self.events = events
        self.assistant = simpy.Resource(env, self.CAPACITY)
        self.requestCount = 0
        self.toRecord = False
        # move just before the first event
        zeroTime = self.events[0] - 1
        env.run(zeroTime)
        i = 0
        for evnt in self.events:
            i += 1
            start_delayed(env, self.accident(env, Call(evnt, i)), evnt - zeroTime)

    def accident(self, env, call):
        # print(tu.getTimeStr(call[0]), "(", call[1], ")", "->", env.now, " start")
        self.requestCount += 1
        qLen = self.getQueueLen()
        if qLen > 0:
            # print(i, "-IN>", env.now, " QUEUE", qLen)
            self.toRecord = True

        with self.assistant.request() as req:
            yield req
            # print(tu.getTimeStr(call[0]), "(", call[1], ")", "->", tu.getTimeStr(env.now), " Calling...")
            yield env.timeout(120)

        self.requestCount -= 1
        # qLen = self.getQueueLen()
        # if qLen>0:
        #     print(i, "-OUT>", env.now, " QUEUE", qLen)
        #     self.toRecord = True

    def getQueueLen(self):
        return self.requestCount - self.CAPACITY
