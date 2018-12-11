import math

import numpy as np
from scipy.optimize import minimize
from shared import SharedOptimizer
from manhattan import Manhattan

# This one does not work - constrains are mostly not handled and require gradient algorithm which complains about singular hessian

CENTERS = 4
ITER = 1



# shared = SharedOptimizer(CENTERS, ITER)
shared = Manhattan(CENTERS, ITER)


def costFunction(centerPoints):
    loss, std = shared.costHelper(centerPoints)
    return loss# +  (std)




# slight modificaiton - if too far from optimum, it is not found :-(
specialInit = [ 1, 1,  1,  2,  3, 3,  10,  10]
specialInit = np.array(specialInit).reshape((CENTERS, 2))

def constraint1(x):
    loss, std = shared.costHelper(x)
    return std


cs = [{"type":"eq","fun":constraint1}]

f = lambda initVal: minimize(costFunction, specialInit, constraints=cs,method="SLSQP", options={"eps": 0.003})

shared.doIt(f)


