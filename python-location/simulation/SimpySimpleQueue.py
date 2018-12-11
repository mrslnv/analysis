import simpy
from simpy.util import start_delayed

CAPACITY = 2


class CallCenter:
    def __init__(self, env, events):
        self.events = events
        self.assistant = simpy.Resource(env, CAPACITY)
        self.requestCount = 0
        self.toRecord = False
        i = 0
        for e in self.events:
            i += 1
            start_delayed(env, self.accident(env, i), e)

    def accident(self, env, i):
        self.requestCount += 1
        qLen = self.getQueueLen()
        if qLen>0:
            # print(i, "-IN>", env.now, " QUEUE", qLen)
            self.toRecord = True

        with self.assistant.request() as req:
            yield req
            # print(i, "->", env.now, " Calling...")
            yield env.timeout(2)

        self.requestCount -= 1
        # qLen = self.getQueueLen()
        # if qLen>0:
        #     print(i, "-OUT>", env.now, " QUEUE", qLen)
        #     self.toRecord = True

    def getQueueLen(self):
        return self.requestCount - CAPACITY


env = simpy.Environment()
# callCenter = CallCenter(env, [2, 5, 5, 6, 6, 6, 6, 7, 7, 7, 9, 11, 13, 15, 19])
# callCenter = CallCenter(env, [1, 1, 1, 1, 1, 1, 7])
callCenter = CallCenter(env, [1, 1, 1, 1, 1, 7, 7,7,12,12,22,22])
for i in range(1, 15):
    callCenter.toRecord = False
    env.run(until=i)
    if callCenter.toRecord:
        print(env.now-1," q ",callCenter.getQueueLen())
