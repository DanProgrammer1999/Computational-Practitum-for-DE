from math import ceil

import plotly.graph_objs as go
import plotly
import numpy as np
import configparser as cnf

config_file = 'Parameters.ini'
section = 'GRAPH'


class Calculator:
    x = None
    x0 = 0
    y0 = 0
    xf = 0
    h = 0

    def __init__(self):
        config = cnf.ConfigParser()
        config.read(config_file)
        self.x0 = float(config[section]['x0'])
        self.xf = float(config[section]['xf'])
        self.y0 = float(config[section]['y0'])
        self.h = float(config[section]['h'])
        self.x = np.arange(self.x0, self.xf, self.h)

    def calculate(self):
        y0 = self.   exact_solution()
        y1 = self.eulers_method()
        y2 = self.improved_eulers_method()
        y3 = self.range_kutta()

        return [y0, y1, y2, y3]

    @staticmethod
    def f(x, y):
        return x/y + y/x

    def eulers_method(self):
        y = []

        prev_y = self.y0
        for x in self.x:
            curr_y = prev_y + self.h*self.f(x, prev_y)
            prev_y = curr_y
            y.append(curr_y)

        return y

    def improved_eulers_method(self):
        y = []
        prev_y = self.y0
        for x in self.x:
            y_temp = prev_y + self.h*self.f(x, prev_y)
            curr_y = prev_y + self.h*(self.f(x, prev_y) + self.f(x + self.h, y_temp))/2
            prev_y = curr_y
            y.append(curr_y)

        return y

    def range_kutta(self):
        y = []
        prev_y = self.y0

        for x in self.x:
            k1 = self.f(x, prev_y)
            k2 = self.f(x + self.h/2, prev_y + self.h*k1/2)
            k3 = self.f(x + self.h/2, prev_y + self.h*k2/2)
            k4 = self.f(x + self.h, prev_y + self.h*k3)

            t = (k1 + 2*k2 + +2*k3 + k4)/6
            curr_y = prev_y + self.h*t
            prev_y = curr_y
            y.append(curr_y)

        return y

    @staticmethod
    def exact_value(x):
        return x*np.sqrt(2*np.log(x) + 1)

    def exact_solution(self):
        y = [self.exact_value(xi) for xi in self.x]
        return y

# x1, y1 = eulers_method(step)
# x2, y2 = improved_eulers_method(step)
# x3, y3 = range_kutta(step)
# x4, y4 = exact_solution(step)
#
# graph1 = go.Scatter(x=x1, y=y1, mode='lines', name='Euler Method')
# graph2 = go.Scatter(x=x2, y=y2, mode='lines', name='Improved Euler Method')
# graph3 = go.Scatter(x=x3, y=y3, mode='lines', name='Range-Kutta Method')
# graph4 = go.Scatter(x=x4, y=y4, mode='lines', name='Exact solution')
#
# data = [graph1, graph2, graph3, graph4]
# print(plotly.offline.plot(data, filename='graph.html', auto_open=False))
