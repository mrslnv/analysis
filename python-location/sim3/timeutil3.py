import calendar
# import time
from datetime import timedelta, datetime

class TimeUtil3:
    def __init__(self, fmt="%Y-%m-%d %H:%M:%S"):
        self.fmt = fmt

    def getTimeSec(self, s):
        return datetime.strptime(s, self.fmt).timestamp()

    def getTimeStr(self, inSec):
        return datetime.strftime(datetime.utcfromtimestamp(inSec),self.fmt)

    def time(self, s):
        return datetime.strptime(s, self.fmt)

    def sec(self, t):
        return t.timestamp()

    def plusHours(self, t, delta):
        return t + timedelta(hours=delta)

tu = TimeUtil3()