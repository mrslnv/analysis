import csv
from pysal.cg.sphere import arcdist, RADIUS_EARTH_KM
from geopy.distance import great_circle

with open('short.csv', 'r') as f:
    # with open('../tz.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skipp header
    # filter: title[starts(EMS)]
    accidentPoints = list(filter(lambda x: x[4].startswith("EMS:"), reader))

print("EMS item count:", len(accidentPoints))

# list: lat, lng, desc, zip, title, time, twp, e

NEW_YORK = [40.678492, -73.899734]

print(arcdist([0,0], NEW_YORK))
print(great_circle([0,0], NEW_YORK))

#this is too much - arc through center?
print(arcdist([40.2978759 , -75.5812935], [40.678492 , -73.899734]))
# this measures distance fine
# great_circle is right
print(great_circle([40.2978759 , -75.5812935], [40.678492 , -73.899734]))

print(arcdist([60 , -70], [60 , -115]))
print(great_circle([60 , -70], [60 , -115]))

for x in accidentPoints:
    print("p1", x[0], ",", x[1], "p2", NEW_YORK[0], ",", NEW_YORK[1],x[3:])
    print(arcdist([float(x[0]), float(x[1])], NEW_YORK))
    print(great_circle([float(x[0]), float(x[1])], NEW_YORK))

