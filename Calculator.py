import numpy as np
import configparser as cnf
from django.utils.functional import cached_property

config_file = 'Parameters.ini'
section = 'CALCULATOR'


class Calculator:
    x = None
    __x0 = 0
    __y0 = 0
    __xf = 0
    __h = 0
    __n_error_steps = 0
    __error0 = 0
    __errorf = 0

    def __init__(self):
        config = cnf.ConfigParser()
        config.read(config_file)
        self.__x0 = float(config[section]['x0'])
        self.__xf = float(config[section]['xf'])
        self.__y0 = float(config[section]['y0'])
        self.__h = float(config[section]['h'])
        self.__n_error_steps = int(config[section]['n_err_steps'])
        self.__error0 = float(config[section]['err_step0'])
        self.__errorf = float(config[section]['err_stepf'])
        self.x = np.arange(self.__x0, self.__xf + self.__h, self.__h)

    @staticmethod
    def f(x, y):
        return x/y + y/x

    @property
    def euler_method(self):
        return self.__euler()

    @property
    def improved_euler_method(self):
        return self.__improved_euler()

    @property
    def runge_kutta(self):
        return self.__runge_kutta()

    @property
    def exact_solution(self):
        return self.__exact()

    def __exact(self, h=None):
        if h is None:
            x = self.x
        else:
            x = np.arange(self.__x0, self.__xf + h, h)

        y = [self.exact_value(xi) for xi in x]

        return np.array(y)

    def __euler(self, h=None):
        if h is None:
            h = self.__h
            x = self.x
        else:
            x = np.arange(self.__x0, self.__xf + h, h)
        y = [self.__y0]

        for i in range(1, len(x)):
            curr_y = y[i - 1] + h*self.f(x[i - 1], y[i - 1])
            y.append(curr_y)
        return np.array(y)

    def __improved_euler(self, h=None):
        if h is None:
            h = self.__h
            x = self.x
        else:
            x = np.arange(self.__x0, self.__xf, h)

        y = [self.__y0]

        for i in range(1, len(x)):
            y_temp = y[i - 1] + h*self.f(x[i - 1], y[i - 1])
            curr_y = y[i - 1] + h*(self.f(x[i - 1], y[i - 1]) + self.f(x[i], y_temp))/2
            y.append(curr_y)
        return np.array(y)

    def __runge_kutta(self, h=None):
        if h is None:
            h = self.__h
            x = self.x
        else:
            x = np.arange(self.__x0, self.__xf, h)

        y = [self.__y0]

        for i in range(1, len(x)):
            k1 = self.f(x[i - 1], y[i - 1])
            k2 = self.f(x[i - 1] + h/2, y[i - 1] + h*k1/2)
            k3 = self.f(x[i - 1] + h/2, y[i - 1] + h*k2/2)
            k4 = self.f(x[i - 1] + h, y[i - 1] + h*k3)

            t = (k1 + 2*k2 + +2*k3 + k4)/6
            curr_y = y[i - 1] + h*t
            y.append(curr_y)

        return np.array(y)

    @staticmethod
    def exact_value(x):
        return x*np.sqrt(2*np.log(x) + 1)

    def euler_error(self):
        return self.__error(self.__euler)

    def improved_euler_error(self):
        return self.__error(self.__improved_euler)

    def runge_kutta_error(self):
        return self.__error(self.__runge_kutta)

    def __error(self, method):
        steps = np.linspace(self.__error0, self.__errorf, self.__n_error_steps)
        error = []
        for step in steps:
            y = method(h=step)
            exact = self.__exact(h=step)
            curr_error = self.__global_error(exact, y)
            error.append(curr_error)

        return steps, np.array(error)

    @staticmethod
    def __global_error(exact, y):
        sum(abs(exact[i] - y[i]) for i in range(len(y)))
        result = 0
        for i in range(len(y)):
            result += abs(exact[i] - y[i])

        return result


c = Calculator()
print(c.euler_method)
