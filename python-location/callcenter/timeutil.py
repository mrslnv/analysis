# import time
from datetime import timedelta, datetime


class TimeUtil:

    def __init__(self, fmt="%Y-%m-%d %H:%M:%S"):
        self.fmt = fmt

    def time_sec(self, s):
        return datetime.strptime(s, self.fmt).timestamp()

    def time_str(self, inSec):
        return datetime.strftime(datetime.utcfromtimestamp(inSec),self.fmt)

    def time(self, s):
        return datetime.strptime(s, self.fmt)

    def sec(self, t):
        return t.timestamp()

    def forward(self, t, delta):
        return t + timedelta(hours=delta)

tu = TimeUtil()