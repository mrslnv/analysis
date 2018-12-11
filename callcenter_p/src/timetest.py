from datetime import timedelta, datetime
from timeutil import tu

t = tu.time_sec("2015-12-14 00:02:01")
print(t)
print(tu.time_str(t))
print(datetime.utcfromtimestamp(t))
#This is wrong
print(datetime.utcfromtimestamp(1450047721))
#This is right
print(datetime.utcfromtimestamp(1450051321))