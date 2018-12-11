import math

import matplotlib.pyplot as plt
import numpy as np
from numpy.random import uniform
from scipy.optimize import minimize
from shared import SharedOptimizer

class Manhattan(SharedOptimizer):
    def __init__(self,CENTERS, ITER):
        super(Manhattan,self).__init__(CENTERS, ITER)

    def distanceFunction(self, a, b):
        return math.fabs(a[0] - b[0])+math.fabs(a[1] - b[1])
