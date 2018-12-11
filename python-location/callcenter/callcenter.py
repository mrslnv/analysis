import simpy
from simpy.util import start_delayed
from collections import namedtuple
from callcenter.timeutil import tu

Call = namedtuple("Call", ["time", "order"])


# adding ability to compute avg wait time
class CallCenter:
    def __init__(self, env, events, capacity=2, qos=20):
        self.CAPACITY = capacity
        self.events = events
        self.assistant = simpy.Container(env, 100,self.CAPACITY)
        self.requestCount = 0
        self.toRecord = False
        self.waitAgg = 0
        self.count = 0
        self.qos = qos
        self.aboveQos = 0

        #schedule calls
        # move just before the first event
        zeroTime = self.events[0] - 1
        env.run(zeroTime)
        i = 0
        for evnt in self.events:
            i += 1
            start_delayed(env, self.accident(env, Call(evnt, i)), evnt - zeroTime)

        #schedule personel shifts
        endTime = self.events[-1]
        t = tu.time("2015-12-14 00:00:00")
        while tu.sec(t) < endTime:
            # mon-fri +1, 10-19
            for i in range(5):
                t = tu.forward(t, 9)
                start_delayed(env, self.assistent_join(env), tu.sec(t) - zeroTime)

                t = tu.forward(t, 1)
                #one more mon - fri, 10-14
                start_delayed(env, self.assistent_join(env), tu.sec(t) - zeroTime)
                t = tu.forward(t, 4)
                start_delayed(env, self.assistent_leave(env), tu.sec(t) - zeroTime)

                t = tu.forward(t, 5)
                start_delayed(env, self.assistent_leave(env), tu.sec(t) - zeroTime)
                t = tu.forward(t, 5)

            # sat-sun +1, 10-18
            for i in range(2):
                t = tu.forward(t, 10)
                start_delayed(env, self.assistent_join(env), tu.sec(t) - zeroTime)
                t = tu.forward(t, 9)
                start_delayed(env, self.assistent_leave(env), tu.sec(t) - zeroTime)
                t = tu.forward(t, 5)

        # t = tu.time("2015-12-14 00:00:00")
        # while tu.sec(t) < endTime:
        #     #mon 3-5
        #     t = tu.plusHours(t,3)
        #     start_delayed(env, self.assistent_join(env), tu.sec(t) - zeroTime)
        #     t = tu.plusHours(t,2)
        #     start_delayed(env, self.assistent_leave(env), tu.sec(t) - zeroTime)
        #     t = tu.plusHours(t,19)
        #
        #     #tue 15-17
        #     t = tu.plusHours(t,15)
        #     start_delayed(env, self.assistent_join(env), tu.sec(t) - zeroTime)
        #     t = tu.plusHours(t,2)
        #     start_delayed(env, self.assistent_leave(env), tu.sec(t) - zeroTime)
        #     t = tu.plusHours(t,7)
        #
        #     t = tu.plusHours(t,24*2)
        #
        #     #fri 15-17
        #     t = tu.plusHours(t,21)
        #     start_delayed(env, self.assistent_join(env), tu.sec(t) - zeroTime)
        #     t = tu.plusHours(t,2)
        #     start_delayed(env, self.assistent_leave(env), tu.sec(t) - zeroTime)
        #     t = tu.plusHours(t,1)
        #
        #     #sat 3-5
        #     t = tu.plusHours(t,3)
        #     start_delayed(env, self.assistent_join(env), tu.sec(t) - zeroTime)
        #     t = tu.plusHours(t,2)
        #     start_delayed(env, self.assistent_leave(env), tu.sec(t) - zeroTime)
        #     t = tu.plusHours(t,19)
        #
        #     #sun 0-1
        #     start_delayed(env, self.assistent_join(env), tu.sec(t) - zeroTime)
        #     t = tu.plusHours(t,1)
        #     start_delayed(env, self.assistent_leave(env), tu.sec(t) - zeroTime)
        #     t = tu.plusHours(t,23)

    def assistent_leave(self,env):
        with self.assistant.get(1) as req:
            yield req

    def assistent_join(self,env):
        with self.assistant.put(1) as req:
            yield req

    def accident(self, env, call):
        # print(tu.getTimeStr(call[0]), "(", call[1], ")", "->", env.now, " start")
        self.requestCount += 1
        qLen = self.getQueueLen()
        if qLen > 0:
            # print(i, "-IN>", env.now, " QUEUE", qLen)
            self.toRecord = True

        startTime = env.now
        with self.assistant.get(1) as req:
            yield req

            wTime = env.now - startTime
            self.waitAgg += wTime
            if wTime > self.qos:
                self.aboveQos += 1

            self.count += 1

            # print(tu.getTimeStr(call[0]), "(", call[1], ")", "->", tu.getTimeStr(env.now), " Calling...")
            yield env.timeout(120)

        with self.assistant.put(1) as req:
            yield req

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
