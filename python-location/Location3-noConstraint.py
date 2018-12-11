import math

import numpy as np
from scipy.optimize import minimize
from shared import SharedOptimizer
from manhattan import Manhattan

# COST == ONLY size difference, "Nelder-Mead" finds a solution in couple steps (for 2, it is perfect)

CENTERS = 5
ITER = 1



# shared = SharedOptimizer(CENTERS, ITER)
shared = Manhattan(CENTERS, ITER)


def costFunction(centerPoints):
    loss, std = shared.costHelper(centerPoints)
    return loss +  std


# 10x10, 4 centers, manhattan - CANNOT FIND OPTIMUM :-(
# specialInit = [ 1, 1,  2,  7,  7, 2,  7,  7]
# specialInit = np.array(specialInit).reshape((CENTERS, 2))
# f = lambda initVal: minimize(costFunction, specialInit, method="Nelder-Mead", options={"maxiter": 125000})


#Very nice
#f = lambda initVal: minimize(costFunction, initVal, method="Nelder-Mead", options={"maxiter": 125000})
#Very nice
 # f = lambda initVal: minimize(costFunction, initVal, method="Powell", options={"maxiter": 125000})
# not so good
# f = lambda initVal: minimize(costFunction, initVal, method="CG", options={"eps": 0.00001})
# not so good
# f = lambda initVal: minimize(costFunction, initVal, method="BFGS", options={"eps": 0.001})

#BUG? Outputs differetn loss but the same points?
# specialInit = [ 7.10316495,  1.91090154,  3.93541901,  4.44172209,  1.47758741,
#                 1.32484204,  7.44783193,  7.18817238,  1.51408096,  7.62263436]
# specialInit = np.array(specialInit).reshape((CENTERS, 2))
# f = lambda initVal: minimize(costFunction, specialInit, method="BFGS", options={"eps": 0.00000001})

# f = lambda initVal: minimize(costFunction, initVal, method="L-BFGS-B", options={"eps": 0.001})
# maybe - sometimes success
# f = lambda initVal: minimize(costFunction, initVal, method="TNC", options={"eps": 0.01})

# works but results?
# f = lambda initVal: minimize(costFunction, initVal, method="COBYLA", options={"maxiter": 250000})

# f = lambda initVal: minimize(costFunction, initVal, method="COBYLA", options={"maxiter": 250000})

# 10x10, 4 centers, FINDS OPTIMUM!!! (3 iterations :-)
# specialInit = [ 1, 1,  2,  7,  7, 2,  7,  7]
# specialInit = np.array(specialInit).reshape((CENTERS, 2))
# f = lambda initVal: minimize(costFunction, specialInit, method="Powell", options={"maxiter": 100000})


# slight modificaiton - if too far from optimum, it is not found :-(
# specialInit = [ 1, 1,  1,  2,  3, 3,  10,  10]
# specialInit = np.array(specialInit).reshape((CENTERS, 2))
# f = lambda initVal: minimize(costFunction, specialInit, method="Powell", options={"maxiter": 100000})

# here, working with 3 centers - it is fine
# specialInit = [ 1, 1,  1,  2,  3, 3]
# specialInit = np.array(specialInit).reshape((CENTERS, 2))
# f = lambda initVal: minimize(costFunction, specialInit, method="Powell", options={"maxiter": 100000})

f = lambda initVal: minimize(costFunction, initVal, method="Powell", options={"maxiter": 100000})
# f = lambda initVal: minimize(costFunction, initVal, method="Nelder-Mead", options={"maxiter": 125000})


# shared.genSymData()
shared.genCenteredData()
shared.doIt(f)


