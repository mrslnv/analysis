from scipy.optimize import minimize

from shared import SharedOptimizer

# COST == ONLY size difference, "Nelder-Mead" finds a solution in couple steps (for 2, it is perfect)

CENTERS = 5
ITER = 20

shared = SharedOptimizer(CENTERS, ITER)

f = lambda initVal: minimize(costFunction, initVal, method="Powell", options={"maxiter": 100000})

def costFunction(centerPoints):
    loss, std = shared.costHelper(centerPoints)
    return std


f = lambda initVal: minimize(costFunction, initVal, method="Nelder-Mead", options={"maxiter": 125000})
shared.doIt(f)
