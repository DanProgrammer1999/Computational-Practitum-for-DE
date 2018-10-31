from Calculator import Calculator
import plotly.graph_objs as go
import plotly
import configparser as cnf

config_file = 'Parameters.ini'
section = 'GRAPH'


class Plotter:
    calculator = None
    __values_filename = ''
    __errors_filename = ''
    __values_mode = ''
    __errors_mode = ''

    def __init__(self, calculator):
        self.calculator = calculator
        config = cnf.ConfigParser()
        config.read(config_file)
        self.__values_filename = config[section]['values_filename']
        self.__errors_filename = config[section]['errors_filename']
        self.__values_mode = config[section]['values_mode']
        self.__errors_mode = config[section]['errors_mode']

    def draw_values(self):
        go_exact = go.Scatter(
            x=self.calculator.x,
            y=self.calculator.exact_solution,
            mode=self.__values_mode,
            name='Exact solution')

        go_euler = go.Scatter(
            x=self.calculator.x,
            y=self.calculator.euler_method,
            mode=self.__values_mode,
            name='Euler method')

        go_improved_euler = go.Scatter(
            x=self.calculator.x,
            y=self.calculator.improved_euler_method,
            mode=self.__values_mode,
            name='Improved Euler Method')

        go_runge_kutta = go.Scatter(
            x=self.calculator.x,
            y=self.calculator.runge_kutta,
            mode=self.__values_mode,
            name='Runge-Kutta method')

        data = [go_exact, go_euler, go_improved_euler, go_runge_kutta]
        plotly.offline.plot(data, filename=self.__values_filename, auto_open=False)

    def draw_errors(self):
        x_euler, y_euler = self.calculator.euler_error()
        x_improved_euler, y_improved_euler = self.calculator.improved_euler_error()
        x_runge_kutta, y_runge_kutta = self.calculator.runge_kutta_error()

        go_euler = go.Scatter(
            x=x_euler,
            y=y_euler,
            mode=self.__errors_mode,
            # xaxis='h',
            # yaxis='Global Error',
            name='Euler method'
        )

        go_improved_euler = go.Scatter(
            x=x_improved_euler,
            y=y_improved_euler,
            mode=self.__errors_mode,
            # xaxis='h',
            # yaxis='Global Error',
            name='Improved Euler method'
        )

        go_runge_kutta = go.Scatter(
            x=x_runge_kutta,
            y=y_runge_kutta,
            mode=self.__errors_mode,
            # xaxis='h',
            # yaxis='Global Error',
            name='Runge-Kutta method'
        )
        data = [go_euler, go_improved_euler, go_runge_kutta]
        plotly.offline.plot(data, filename=self.__errors_filename, auto_open=False)


c = Calculator()
p = Plotter(c)
p.draw_values()
p.draw_errors()


