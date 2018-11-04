import configparser as cnf

import numpy as np

config_file = 'Parameters.ini'
section = 'CALCULATOR'


class Calculator:
    """
    A class that contains all necessary tools to perform all the needed calculations
    in this assignment. It has two separate classes for calculating values and errors,
    and public interface to access the calculations.
    """

    def __init__(self):
        self.__values = self.__Values()
        self.__errors = self.__Errors(self.__values)

    def update(self):
        self.__values = self.__Values()
        self.__errors = self.__Errors(self.__values)

    def x(self):
        return self.__values.x

    def error_steps(self):
        return self.__errors.error_x

    def get_values(self):
        exact = self.__values.exact_solution()
        euler = self.__values.euler_method()
        improved_euler = self.__values.improved_euler_method()
        runge_kutta = self.__values.runge_kutta_method()

        return [exact, euler, improved_euler, runge_kutta]

    def get_errors(self):
        euler = self.__errors.euler_error()
        improved_euler = self.__errors.improved_euler_error()
        runge_kutta = self.__errors.runge_kutta_error()

        return [euler, improved_euler, runge_kutta]

    class __Values:

        __section = "VALUES"

        def __init__(self):
            config = cnf.ConfigParser()
            config.read(config_file)

            self.__h = float(config[self.__section]['h'])
            self.__x0 = float(config[self.__section]['x0'])
            self.__xf = float(config[self.__section]['xf'])
            self.__y0 = float(config[self.__section]['y0'])
            self.x = np.arange(self.__x0, self.__xf + self.__h, self.__h)

        def exact_solution(self, h=None):
            """
            Calculate an exact solution for each x in the given grid.
            :param h: Specify a custom step.
            :return: A set of y(x) for each x given by the parameters.
            """
            if h is None:
                x = self.x
            else:
                x = np.arange(self.__x0, self.__xf + h, h)

            y = [self.exact_value(xi) for xi in x]

            return np.array(y)

        def euler_method(self, h=None):
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

        def improved_euler_method(self, h=None):
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

        def runge_kutta_method(self, h=None):
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
        def f(x, y):
            return x/y + y/x

        @staticmethod
        def exact_value(x):
            return x*np.sqrt(2*np.log(x) + 1)

    class __Errors:

        __section = "ERRORS"

        def __init__(self, values):

            config = cnf.ConfigParser()
            config.read(config_file)
            error_mode = config[self.__section]['err_mode']

            self.__values = values

            self.__n_error_steps = int(config[self.__section]['n_err_steps'])
            self.__error_step = float(config[self.__section]['err_step'])
            self.__error0 = float(config[self.__section]['err0'])
            self.__errorf = float(config[self.__section]['errf'])

            if error_mode == 'linspace':
                self.error_x = np.linspace(self.__error0, self.__errorf, self.__n_error_steps)
            else:
                self.error_x = np.arange(self.__error0, self.__errorf + self.__error_step, self.__error_step)

        def euler_error(self):
            """
            Calculate a list of maximum local errors for different grid sizes for Improved Euler method.
            :return: A list of maximum local errors for different grid sizes for Improved Euler method.
            """
            return self.__error(self.__values.euler_method)

        def improved_euler_error(self):
            """
            Calculate a list of maximum local errors for different grid sizes for Improved Euler method.
            :return: A list of maximum local errors for different grid sizes for Improved Euler method.
            """
            return self.__error(self.__values.improved_euler_method)

        def runge_kutta_error(self):
            """
            Calculate a list of maximum local errors for different grid sizes for Runge-Kutta method.
            :return: A list of maximum local errors for different grid sizes for Runge-Kutta method.
            """
            return self.__error(self.__values.runge_kutta_method)

        def __error(self, method):
            """
            Find a list of maximum local errors for different grid sizes for a given approximation method.
            :param method: Approximation method to find the error of.
            :return: A list of maximum local errors for different grid sizes.
            """
            steps = self.error_x
            error = []

            for step in steps:
                y = method(h=step)
                exact = self.__values.exact_solution(h=step)
                curr_error = self.__maximum_error(exact, y)
                error.append(curr_error)

            return np.array(error)

        @staticmethod
        def __local_error(exact, y):
            """
            Calculate a local error, which is just the list of differences between each exact_i and y_i.
            :param exact: The exact solution of the equation for a given grid size.
            :param y: An approximated solution for a given grid size.
            :return: A list of local errors for each point of the grid.
            """
            return [abs(y[i] - exact[i]) for i in range(len(y))]

        def __maximum_error(self, exact, y):
            """
            Find the maximum local error for the exact and an approximated solution.
            :param exact: The exact solution of the equation for a given grid size.
            :param y: An approximated solution for a given grid size.
            :return: A maximum local error from the list of local errors.
            """
            return max(self.__local_error(exact, y))
