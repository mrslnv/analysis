import simpy
from simpy.util import start_delayed
from collections import namedtuple
from simulation.timeutil import tu

Call = namedtuple("Call", ["time", "order"])


# adding ability to compute avg wait time
class CallCenter:
    def __init__(self, env, events, capacity=2, qos=20):
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
        self.waitAgg = 0
        self.count = 0
        self.qos = qos
        self.aboveQos = 0

    def accident(self, env, call):
        # print(tu.getTimeStr(call[0]), "(", call[1], ")", "->", env.now, " start")
        self.requestCount += 1
        qLen = self.getQueueLen()
        if qLen > 0:
            # print(i, "-IN>", env.now, " QUEUE", qLen)
            self.toRecord = True

        startTime = env.now
        with self.assistant.request() as req:
            yield req

            wTime = env.now - startTime
            self.waitAgg += wTime
            if wTime > self.qos:
                self.aboveQos += 1

            self.count += 1

            # print(tu.getTimeStr(call[0]), "(", call[1], ")", "->", tu.getTimeStr(env.now), " Calling...")
            yield env.timeout(120)


        self.requestCount -= 1
        # qLen = self.getQueueLen()
        # if qLen>0:
        #     print(i, "-OUT>", env.now, " QUEUE", qLen)
        #     self.toRecord = True

    def getQueueLen(self):
        return self.requestCount - self.CAPACITY

    def getAvgWait(self):
        return self.waitAgg / self.count

    def getQoS(self):
        return 100*(1 - self.aboveQos / self.count)
