import math

import matplotlib.pyplot as plt
import numpy as np
from numpy.random import uniform
from scipy.optimize import minimize


class SharedOptimizer:
    def __init__(self, CENTERS, ITER):
        self.centerSize = [0] * CENTERS
        self.centersTmp = [[0] * 2] * CENTERS
        self.CENTERS = CENTERS
        self.ITER = ITER
        self.centersTmp = [[0]*2]*CENTERS

    def costHelper(self,centerPoints):
        for i in range(len(self.centerSize)):
            self.centerSize[i] = 0

        centerPoints = np.array(centerPoints).reshape((self.CENTERS, 2))

        # print("x",centerPoints)

        # i = 0
        # for old,new in zip(self.centersTmp, centerPoints):
        #     print("Move x=",old[0]-new[0],"y=",old[1]-new[1])
        #     self.centersTmp[i] = [new[0],new[1]]
        #     i += 1

        loss = 0
        for point in self.inputData:
            minDist = math.inf
            idx = -1
            for i, center in enumerate(centerPoints):
                dist = self.distanceFunction(center, point)
                if dist < minDist:
                    minDist = dist
                    idx = i

            loss += minDist
            self.centerSize[idx] += 1

        std = np.std(self.centerSize)

        print("cost:",loss,std)
        return loss, std

    def genSymData(self):
        data = []

        for x in range(10):
            for y in range(10):
                data.append([x, y])

        self.inputData = data
        return data

    def genCenteredData(self):
        centers = [[2,2],[2,8],[8,2],[8,8],[5,5]]
        data = []

        for point in centers:
            for i in range(8):
                x = point[0] + math.cos(i * math.pi / 4)
                y = point[1] + math.sin(i * math.pi / 4)
                data.append([x, y])

        self.inputData = data
        return centers

    def drawPlot(self, centers,xlim = [-1,11], ylim = [-1,11]):
        points = self.inputData
        # define grid.
        xi = [point[0] for point in points]
        yi = [point[1] for point in points]
        # plot data points.
        plt.scatter(xi, yi, s=5, marker='o', c='b')
        centers = np.array(centers).reshape(2*self.CENTERS,1)
        cx = centers[0:][::2]
        cy = centers[1:][::2]
        plt.scatter(cx, cy, s=10, marker='o', c='r')
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.title('griddata test')
        plt.show()

    def distanceFunction(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def runOptimization(self, minMethod):
        best = None
        bestCenterSize = None
        opt = math.inf
        for i in range(self.ITER):
            initValues = self.genInitData()
            # optimization = minimize(costFunction, initValues, method="Nelder-Mead", options={"maxiter": 150000})
            optimization = minMethod(initValues)

            print("Optimum:", optimization.fun, " existing min:", opt)
            print("Size:", self.centerSize)
            if optimization.fun < opt:
                opt = optimization.fun
                best = optimization
                bestCenterSize = self.centerSize[:]

                # drawPlot(inputData, optX)

        return best, bestCenterSize

    def genInitData(self):
        return [(uniform(0, 10), uniform(0, 10)) for x in range(self.CENTERS)]

    def doIt(self, minMethod):
        opt = math.inf

        self.best, self.bestCenterSize = self.runOptimization(minMethod)

        print(self.best)
        print("Cost", self.best.fun)
        print("Size", self.bestCenterSize, np.std(self.bestCenterSize))
        dist, std = self.costHelper(self.best.x)
        print("Dist",dist,"Std",std)

        self.drawPlot(self.best.x)


# ======================================
# f = lambda initVal: minimize(lambda x:x, initVal, method="Nelder-Mead", options={"maxiter": 150000})
# x = SharedOptimizer(5,30,f)
# x.doIt()
