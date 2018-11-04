import configparser as cnf

import plotly
import plotly.graph_objs as go

from Calculator import Calculator

config_file = 'Parameters.ini'
section = 'GRAPH'


class Plotter:

    def __init__(self, calculator):
        self.calculator = calculator
        config = cnf.ConfigParser()
        config.read(config_file)
        self.__values_filename = config[section]['values_filename']
        self.__errors_filename = config[section]['errors_filename']
        self.__values_mode = config[section]['values_mode']
        self.__errors_mode = config[section]['errors_mode']

    def update(self):
        self.draw_errors()
        self.draw_errors()

    def draw_values(self):
        values = self.calculator.get_values()

        go_exact = go.Scatter(
            x=self.calculator.x(),
            y=values[0],
            mode=self.__values_mode,
            name='Exact solution')

        go_euler = go.Scatter(
            x=self.calculator.x(),
            y=values[1],
            mode=self.__values_mode,
            name='Euler method')

        go_improved_euler = go.Scatter(
            x=self.calculator.x(),
            y=values[2],
            mode=self.__values_mode,
            name='Improved Euler Method')

        go_runge_kutta = go.Scatter(
            x=self.calculator.x(),
            y=values[3],
            mode=self.__values_mode,
            name='Runge-Kutta method')

        data = [go_exact, go_euler, go_improved_euler, go_runge_kutta]
        plotly.offline.plot(data, filename=self.__values_filename, auto_open=False)

    def draw_errors(self):
        x = self.calculator.error_steps()
        errors = self.calculator.get_errors()

        go_euler = go.Scatter(
            x=x,
            y=errors[0],
            mode=self.__errors_mode,
            name='Euler method'
        )

        go_improved_euler = go.Scatter(
            x=x,
            y=errors[1],
            mode=self.__errors_mode,
            name='Improved Euler method'
        )

        go_runge_kutta = go.Scatter(
            x=x,
            y=errors[2],
            mode=self.__errors_mode,
            name='Runge-Kutta method'
        )
        data = [go_euler, go_improved_euler, go_runge_kutta]
        plotly.offline.plot(data, filename=self.__errors_filename, auto_open=False)


c = Calculator()
p = Plotter(c)
p.draw_values()
p.draw_errors()
