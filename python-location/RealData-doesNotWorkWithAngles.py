import csv
import math
from geopy.distance import great_circle
from shared import SharedOptimizer
from scipy.optimize import minimize

#This does not work. When it hops through points, it goes to funny angles 525
class GlobeOptimizer(SharedOptimizer):
    def __init__(self, CENTERS, ITER):
        super(GlobeOptimizer, self).__init__(CENTERS, ITER)

    def distanceFunction(self, a, b):
        return great_circle(a, b).km

    # data[x(lng),y(lat)]
    def init(self, data):
        opt.inputData = data
        lng = [float(point[0]) for point in data]
        lat = [float(point[1]) for point in data]
        self.lngMax = max(lng)
        self.lngMin = min(lng)
        self.latMax = max(lat)
        self.latMin = min(lat)

    def latRel(self, r):
        return self.latMin + r * (self.latMax - self.latMax)

    def lngRel(self, r):
        return self.lngMin + r * (self.lngMax - self.lngMax)

    def genInitData(self):
        return [
            [self.lngRel(0.05),self.latRel(0.55)],
            [self.lngRel(0.35),self.latRel(0.3)],
            [self.lngRel(0.45),self.latRel(0.3)],
            [self.lngRel(0.7),self.latRel(0.35)],
            [self.lngRel(0.7),self.latRel(0.25)]
            ]

    def drawPlot(self, centers,xlim = [-1,11], ylim = [-1,11]):
        super(GlobeOptimizer, self).drawPlot(centers, [self.lngMin,self.lngMax],[self.latMin,self.latMax])


# with open('short.csv', 'r') as f:
# with open('../tz.csv', 'r') as f:
#     reader = csv.reader(f)
#     next(reader)  # skipp header
#     accidentPoint = list(filter(lambda x: x[4].startswith("EMS:"), reader))
with open('../emergency-clean.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skipp header
    accidentPoint = list(reader)

# list: lat, lng, desc, zip, title, time, twp, e

print("EMS item count:", len(accidentPoint))

CENTERS = 5
ITER = 1

opt = GlobeOptimizer(CENTERS, ITER)


def costFunction(centerPoints):
    loss, std = opt.costHelper(centerPoints)
    return loss + std


opt.init([[float(a[1]), float(a[0])] for a in accidentPoint])
f = lambda initVal: minimize(costFunction, initVal, method="Powell", options={"maxiter": 100000})
opt.doIt(f)
