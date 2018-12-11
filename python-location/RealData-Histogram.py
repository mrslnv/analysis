import csv
from pysal.cg.sphere import arcdist, RADIUS_EARTH_KM
from geopy.distance import great_circle
import matplotlib.pyplot as plt

# with open('short.csv', 'r') as f:
with open('../tz.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skipp header
    # filter: title[starts(EMS)]
    accidentPoints = list(filter(lambda x: x[4].startswith("EMS:"), reader))

print("EMS item count:", len(accidentPoints))

# list: lat, lng, desc, zip, title, time, twp, e


points = accidentPoints
# define grid.
xi = [float(point[1]) for point in points]
yi = [float(point[0]) for point in points]
plt.hist(xi, 50, normed=1, facecolor='green', alpha=0.75)
plt.show()
plt.hist(yi, 50, normed=1, facecolor='green', alpha=0.75)
plt.show()

# plot data points.
plt.scatter(xi, yi, s=5, marker='o', c='b')
plt.xlim(-74, -76)
plt.ylim(39.5, 41.5)
plt.title('griddata test')
plt.show()
