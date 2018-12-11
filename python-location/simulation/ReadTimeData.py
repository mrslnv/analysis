import csv
import calendar
import time

class TimeUtil:
    def __init__(self,fmt = "%Y-%m-%d %H:%M:%S"):
        self.fmt = fmt

    def getTimeSec(self,s):
        return calendar.timegm(time.strptime(s,self.fmt))

    def getTimeStr(self,inSec):
        return time.strftime(self.fmt,time.gmtime(inSec))

with open('time.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skipp header
    td = list(reader)

tu = TimeUtil()
s = "2015-12-14 00:02:01"
t = tu.getTimeSec(s)
print(s, t, tu.getTimeStr(t))
s = td[0][1]
t = tu.getTimeSec(s)
print(s, t, tu.getTimeStr(t))
s = "2015-12-14 00:02:02"
t = tu.getTimeSec(s)
print(s, t, tu.getTimeStr(t))
