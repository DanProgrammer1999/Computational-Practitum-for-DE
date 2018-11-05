import configparser as cnf

import numpy as np
from functools import lru_cache

config_file = 'Parameters.ini'

class Calculator:
    """
    A class that contains all necessary tools to perform all the needed calculations
    in this assignment. It has two separate classes for calculating values and errors,
    and public interface to access the calculations.
    """
    __section = "CALCULATOR"

    def __init__(self):
        """
        Initialize an object of class Calculator.
        Create and initialize two instances of each of Calculator's subclasses: Values and Errors.
        """
        self.__values = self.Values()
        self.__errors = self.Errors(self.__values)

    @property
    def x(self):
        """
        Get the list of values used by numerical methods for the calculations of the approximated results.
        :return: A list of values which gives the x axis for the values and local error graphs.
        """
        return self.__values.x

    @property
    def global_errors_x(self):
        """
        Get the list of steps for which the maximum error was calculated.
        :return: A list of values which gives the x axis for the global (maximum) error graph.
        """
        return self.__errors.error_x

    def get_values(self):
        """
        Returns a list of calculates for each approximation method
        given by the specification of the assignment.
        :return: A list l of four lists, each consisting of calculation results
        for specific computational method, namely:
            l[0] - values for the exact solution;
            l[1] - values for Euler method;
            l[2] - values for Improved Euler method;
            l[3] - values for Runge-Kutta method.
        """
        exact = self.__values.exact_solution()
        euler = self.__values.euler_method()
        improved_euler = self.__values.improved_euler_method()
        runge_kutta = self.__values.runge_kutta_method()

        return [exact, euler, improved_euler, runge_kutta]

    def get_local_errors(self):
        """
        Returns a list of local errors for each approximation method
        given by the specification of the assignment.
        :return: A list l of three lists, each consisting of local errors
        for specific computational method, namely:
            l[0] - local errors for Euler method;
            l[1] - local errors for Improved Euler method;
            l[2] - local errors for Runge-Kutta method.
        """
        euler = self.__errors.euler_local()
        improved_euler = self.__errors.improved_euler_local()
        runge_kutta = self.__errors.runge_kutta_local()

        return [euler, improved_euler, runge_kutta]

    def get_global_errors(self):
        euler = self.__errors.euler_global()
        improved_euler = self.__errors.improved_euler_global()
        runge_kutta = self.__errors.runge_kutta_global()

        return [euler, improved_euler, runge_kutta]

    class Values:
        """
        A subclass of class Calculator to encapsulate the values-specific calculations.
        """

        __section = "VALUES"

        def __init__(self):
            """
            Initialize an object of class Calculator.Values.
            Read all important information from the config and create class variables for it.
            """
            config = cnf.ConfigParser()
            config.read(config_file)

            self.__h = float(config[self.__section]['h'])
            self.__x0 = float(config[self.__section]['x0'])
            self.__xf = float(config[self.__section]['xf'])
            self.__y0 = float(config[self.__section]['y0'])
            self.x = np.arange(self.__x0, self.__xf + self.__h, self.__h)

        @lru_cache(maxsize=1)
        def exact_solution(self, h=None):
            """
            Calculate an exact solution for the given grid.
            The "default" result of the function (i.e. for the values and local error graphs) is cached
            in order to avoid repeating heavy calculations.
            :param h: Specify a custom step (by default it is specified by the config file).
            :return: A set of y(x) for each x given by the parameters.
            """
            if h is None:
                x = self.x
            else:
                x = np.arange(self.__x0, self.__xf + h, h)

            y = [self.exact_value(xi) for xi in x]

            return np.array(y)

        @lru_cache(maxsize=1)
        def euler_method(self, h=None):
            """
            Calculate an approximated result given by Euler method for the given grid.
            The "default" result of the function (i.e. for the values and local error graphs) is cached
            in order to avoid repeating heavy calculations.
            :param h: Specify a custom step (by default it is specified by the config file).
            :return: A set of steps calculated by Euler method leading
            from initial value to final value with step h.
            """
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

        @lru_cache(maxsize=1)
        def improved_euler_method(self, h=None):
            """
            Calculate an approximated result given by Improved Euler method for the given grid.
            The "default" result of the function (i.e. for the values and local error graphs) is cached
            in order to avoid repeating heavy calculations.
            :param h: Specify a custom step (by default it is specified by the config file).
            :return: A set of steps calculated by Improved Euler method leading
            from initial value to final value with step h.
            """
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

        @lru_cache(maxsize=1)
        def runge_kutta_method(self, h=None):
            """
            Calculate an approximated result given by Runge-Kutta method for the given grid.
            The "default" result of the function (i.e. for the values and local error graphs) is cached
            in order to avoid repeating heavy calculations.
            :param h: Specify a custom step (by default it is specified by the config file).
            :return: A set of steps calculated by Runge-Kutta method leading
            from initial value to final value with step h.
            """
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
            """
            Calculate a function f(x), such that for the given x and y
            the result equals to y'(x, y) for the given equation.
            :param x: value of x.
            :param y: value of y.
            :return: y'(x, y), where y' is given by the assignment specifications.
            """
            return x/y + y/x

        @staticmethod
        def exact_value(x):
            """
            A formula for the exact solution for the given differential equation.
            :param x: value of x.
            :return: y(x), where y is given by the solution to the D.E. specified by the assignment.
            """
            return x*np.sqrt(2*np.log(x) + 1)

    class Errors:
        """
        A subclass of class Calculator to encapsulate the errors-specific calculations.
        """

        __section = "ERRORS"

        def __init__(self, values):
            """
            Initialize an object of class Calculator.Errors.
            Read all important information from the config and create class variables for it.
            :param values (Calculator.__Values): An instance of subclass __Values of class Calculator.
            """

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

        def euler_local(self):
            """
            Calculate a list of local errors for the Euler approximation method
            (the result is given by __local_error function).
            :return: List of local errors for the Euler method.
            """
            return self.__local_error(self.__values.exact_solution(), self.__values.euler_method())

        def improved_euler_local(self):
            """
            Calculate a list of local errors for the Improved Euler approximation method
            (the result is given by __local_error function).
            :return: List of local errors for the Improved Euler method.
            """
            return self.__local_error(self.__values.exact_solution(), self.__values.improved_euler_method())

        def runge_kutta_local(self):
            """
            Calculate a list of local errors for the Runge-Kutta approximation method
            (the result is given by __local_error function).
            :return: List of local errors for the Runge-Kutta method.
            """
            return self.__local_error(self.__values.exact_solution(), self.__values.runge_kutta_method())

        def euler_global(self):
            """
            Calculate a list of maximum local errors for different grid sizes for Improved Euler method.
            :return: A list of maximum local errors for different grid sizes for Improved Euler method.
            """
            return self.__global_error(self.__values.euler_method)

        def improved_euler_global(self):
            """
            Calculate a list of maximum local errors for different grid sizes for Improved Euler method.
            :return: A list of maximum local errors for different grid sizes for Improved Euler method.
            """
            return self.__global_error(self.__values.improved_euler_method)

        def runge_kutta_global(self):
            """
            Calculate a list of maximum local errors for different grid sizes for Runge-Kutta method.
            :return: A list of maximum local errors for different grid sizes for Runge-Kutta method.
            """
            return self.__global_error(self.__values.runge_kutta_method)

        @staticmethod
        def __local_error(exact, y):
            """
            Calculate a local error (i.e. a list of values abs(exact[i] - y[i]) for each i).
            :param exact: The exact solution of the equation for a given grid size.
            :param y: An approximated solution for a given grid size.
            :return: A list of local errors for each point of the grid.
            """
            return [abs(y[i] - exact[i]) for i in range(len(y))]

        @staticmethod
        def __maximum_error(exact, y):
            """
            Find the maximum local error for the exact and an approximated solution.
            :param exact: The exact solution of the equation for a given grid size.
            :param y: An approximated solution for a given grid size.
            :return: A maximum local error from the list of local errors.
            """
            return max(Calculator.Errors.__local_error(exact, y))

        def __global_error(self, method):
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
