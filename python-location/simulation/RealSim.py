import csv
from simulation.simqueue import CallCenter
import simpy
import itertools
import math
from simulation.timeutil import tu


with open('time.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skipp header
    td = list(reader)

# td = td[:100]

env = simpy.Environment()
events = [tu.getTimeSec(evnt[1]) for evnt in td]
callCenter = CallCenter(env, events, 2)
i = events[0] + 1
print("Start time:",tu.getTimeStr(i))
q = []
while True:
    callCenter.toRecord = False

    env.run(until=i)

    if callCenter.toRecord:
        qLen = callCenter.getQueueLen()
        # print(env.now - 1, " q ", qLen)
        if qLen > 0:
            q.append([tu.getTimeStr(env.now-1), qLen])

    peek = env.peek()
    if peek == math.inf:
        break
    i = peek+1
    # print("next time:",tu.getTimeStr(i))
    # if i>tu.getTimeSec("2016-02-01 00:00:00"):
    #     break;

# for qr in q:
#     print(qr[0],qr[1])

with open("q2-output.csv", "w",newline="") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for qr in q:
        writer.writerow(qr)

