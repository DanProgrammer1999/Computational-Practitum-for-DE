from math import ceil

import matplotlib.pyplot as plot
import numpy as np

x0 = 1
y0 = 1
xf = 2.3


def f(x, y):
    return x / y + y / x


def eulers_method(step):
    x = np.arange(x0, xf + step, step=step, dtype=float)
    y = np.array([y0] * len(x), dtype=float)

    for i in range(1, len(x)):
        y[i] = y[i - 1] + step*f(x[i - 1], y[i - 1])

    return x, y


x, y = eulers_method(1e-5)

plot.plot(list(x), list(y))
plot.title("Euler's method")
plot.show()


x1, y1 = eulers_method(1e-3)

plot.plot(x1, y1)
plot.title("Euler's method")
plot.show()


error = abs(y1[-1] - y[-1])

print(error)

