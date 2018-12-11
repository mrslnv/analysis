import math

import matplotlib.pyplot as plt
import numpy as np
from numpy.random import uniform
from scipy.optimize import minimize


# COST == ONLY distance, CONSTRAINT == equality - STD, no convergency

CENTERS = 5
ITER = 1


def genSymData():
    data = []

    for x in range(10):
        for y in range(10):
            data.append([x, y])

    return data


def drawPlot(points, centers):
    # define grid.
    xi = [point[0] for point in points]
    yi = [point[1] for point in points]
    # plot data points.
    plt.scatter(xi, yi, s=5, marker='o', c='b')
    cx = centers[0:][::2]
    cy = centers[1:][::2]
    plt.scatter(cx, cy, s=10, marker='o', c='r')
    plt.xlim(-1, 11)
    plt.ylim(-1, 11)
    plt.title('griddata test')
    plt.show()


inputData = genSymData()
opt = math.inf
optX = []
centerSize = [0]*CENTERS

def distanceFunction(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def costFunction(centerPoints):
    centerPoints = np.array(centerPoints).reshape((CENTERS, 2))
    loss = 0
    for point in inputData:
        minDist = math.inf
        idx = -1
        for i, center in enumerate(centerPoints):
            dist = distanceFunction(center, point)
            if dist < minDist:
                minDist = dist
                idx = i

        loss += minDist
        centerSize[idx] += 1

    print("x",centerPoints)
    print("loss",loss)
    return loss

def constraintSize(centerPoints):
    centerSize = [0]*CENTERS
    centerPoints = np.array(centerPoints).reshape((CENTERS, 2))
    loss = 0
    for point in inputData:
        minDist = math.inf
        idx = -1
        for i, center in enumerate(centerPoints):
            dist = distanceFunction(center, point)
            if dist < minDist:
                minDist = dist
                idx = i

        loss += minDist
        centerSize[idx] += 1

    print("diff",centerSize)
    return np.std(centerSize)


cs = [{"type":"eq","fun":constraintSize}]

for i in range(ITER):
    initValues = [(uniform(0, 10), uniform(0, 10)) for x in range(CENTERS)]
    optimization = minimize(costFunction, initValues, constraints=cs)

    print("Optimum:", optimization.fun)
    if optimization.fun < opt:
        opt = optimization.fun
        optX = optimization.x

    drawPlot(inputData, optX)

print(optimization)
print("Size",centerSize )
print("Size diff",np.std(centerSize ))

drawPlot(inputData, optX)
