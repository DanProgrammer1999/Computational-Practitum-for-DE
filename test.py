from math import ceil

import plotly.graph_objs as go
import plotly
import numpy as np
import cufflinks as cf


x0 = 1
y0 = 1
xf = 2.3
step = 1e-4


def f(x, y):
    return x/y + y/x


def eulers_method(step):
    x = np.arange(x0, xf + step, step=step, dtype=float)
    y = np.array([y0]*len(x), dtype=float)

    for i in range(1, len(x)):
        y[i] = y[i - 1] + step*f(x[i - 1], y[i - 1])

    return x, y


def improved_eulers_method(step):
    x = np.arange(x0, xf + step, step=step, dtype=float)
    y = np.array([y0]*len(x), dtype=float)

    for i in range(1, len(x)):
        y[i] = y[i - 1] + step*f(x[i - 1], y[i - 1])
        y[i] = y[i - 1] + step*(f(x[i - 1], y[i - 1]) + f(x[i], y[i]))/2

    return x, y


def range_kutta(step):
    x = np.arange(x0, xf + step, step=step, dtype=float)
    y = np.array([y0]*len(x), dtype=float)

    for i in range(1, len(x)):
        k1 = f(x[i - 1], y[i - 1])
        k2 = f(x[i - 1] + step/2, y[i - 1] + step*k1/2)
        k3 = f(x[i - 1] + step/2, y[i - 1] + step*k2/2)
        k4 = f(x[i - 1] + step, y[i - 1] + step*k3)

        t = (k1 + 2*k2 + +2*k3 + k4)/6

        y[i] = y[i - 1] + step*t

    return x, y


def exact_value(x):
    return x*np.sqrt(2*np.log(x) + 1)


def exact_solution(step):
    x = np.arange(x0, xf + step, step=step, dtype=float)
    y = [exact_value(xi) for xi in x]
    return x, y


x1, y1 = eulers_method(step)
x2, y2 = improved_eulers_method(step)
x3, y3 = range_kutta(step)
x4, y4 = exact_solution(step)

graph1 = cf.Scatter(x=x1, y=y1, mode='lines', name='Euler Method')
graph2 = cf.Scatter(x=x2, y=y2, mode='lines', name='Improved Euler Method')
graph3 = cf.Scatter(x=x3, y=y3, mode='lines', name='Range-Kutta Method')
graph4 = cf.Scatter(x=x4, y=y4, mode='lines', name='Exact solution')

data = [graph1, graph2, graph3, graph4]
print(plotly.offline.plot(data))
