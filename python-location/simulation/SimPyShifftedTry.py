import csv
import calendar
import time
import simpy

class TimeUtil:
    def __init__(self,fmt = "%Y-%m-%d %H:%M:%S"):
        self.fmt = fmt

    def getTimeSec(self,s):
        return calendar.timegm(time.strptime(s,self.fmt))

    def getTimeStr(self,inSec):
        return time.strftime(self.fmt,time.gmtime(inSec))


tu = TimeUtil()
s = "2015-12-14 00:02:01"
t = tu.getTimeSec(s)

def example(env):
    event = simpy.events.Timeout(env, delay=1, value=42)
    value = yield event
    print('now=%d, value=%d' % (env.now, value))
 
env = simpy.Environment()
example_gen = example(env)
# p = simpy.events.Process(env, example_gen)

print("start")
env.run(t)
print("end",env.now)
p = simpy.events.Process(env, example_gen)
env.run(t+2)
print("event done",env.now)
