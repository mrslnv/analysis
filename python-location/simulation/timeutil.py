import calendar
import time

class TimeUtil:
    def __init__(self, fmt="%Y-%m-%d %H:%M:%S"):
        self.fmt = fmt

    def getTimeSec(self, s):
        return calendar.timegm(time.strptime(s, self.fmt))

    def getTimeStr(self, inSec):
        return time.strftime(self.fmt, time.gmtime(inSec))

    def time(self, s):
        return time.strptime(s, self.fmt)

    def sec(self, t):
        pass

    def plusHours(self, t, delta):
        pass

tu = TimeUtil()