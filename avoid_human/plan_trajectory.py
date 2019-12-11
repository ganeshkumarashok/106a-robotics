#!/usr/bin/env python
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.optimize import LinearConstraint, NonlinearConstraint, minimize


def plan_trajectory(human, robot, dist_fun, R, N, M):
    t = lambda x, v, i: np.sum(np.diff(x[:i + 1]) / v[:i])
    f = lambda v, x: t(x, v, N) / 10000000 # https://stackoverflow.com/a/36685019
    x = np.linspace(0, 1, N + 1)
    g = lambda i: lambda v: euclidean(*human(t(x, v, i)), *robot(x[i]))
    nlc = [NonlinearConstraint(g(i), R, np.Inf) for i in range(N + 1)]
    cons = nlc
    results = minimize(f, np.ones(N) * M, bounds=[(0, M) for i in range(N)], constraints=cons, args=x)
    if results.success:
        return results.x, t(np.linspace(0, 1, N + 1), results.x, N)
    else:
        print(results.message)
        return None


if __name__ == '__main__':

    R = 0.2 # Minimum euclidean distance to keep between a human and a robot
    N = 20 # Number of steps to consider in discretization
    M = 0.05 # Maximum speed

    def human(t):
        if t >= 10:
            return (2, 0.5)
        else:
            return (0.1 * t, 0.5)

    robot = lambda x: (0.5, x)

    euclidean = lambda x1, y1, x2, y2: np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    v, t = plan_trajectory(human, robot, euclidean, R, N, M)

    print('Time taken to complete path:', t)
    print(v)
