import configparser as cnf
import plotly
import plotly.graph_objs as go

config_file = 'Parameters.ini'


class Plotter:
    """
    A class that is responsible for creating graphs for values, local and global errors.
    """
    __section = "GRAPH"

    def __init__(self, calculator):
        """
        Initialize an instance of the Plotter class. Read the config for the specific settings.
        Create global variables for an instance of calculator and other important data.
        :param calculator: An instance of class Calculator.
        """
        self.calculator = calculator
        config = cnf.ConfigParser()
        config.read(config_file)
        self.__values_filename = config[self.__section]['values_filename']
        self.__local_errors_filename = config[self.__section]['local_errors_filename']
        self.__global_errors_filename = config[self.__section]['global_errors_filename']
        self.__values_mode = config[self.__section]['values_mode']
        self.__errors_mode = config[self.__section]['errors_mode']

    def draw_values(self):
        """
        Create a graph of values (data is given by the instance of class Calculator)
        """
        x = self.calculator.x
        values = self.calculator.get_values()

        go_exact = go.Scatter(
            x=x,
            y=values[0],
            mode=self.__values_mode,
            name='Exact solution')

        go_euler = go.Scatter(
            x=x,
            y=values[1],
            mode=self.__values_mode,
            name='Euler method')

        go_improved_euler = go.Scatter(
            x=x,
            y=values[2],
            mode=self.__values_mode,
            name='Improved Euler Method')

        go_runge_kutta = go.Scatter(
            x=x,
            y=values[3],
            mode=self.__values_mode,
            name='Runge-Kutta method')

        data = [go_exact, go_euler, go_improved_euler, go_runge_kutta]
        plotly.offline.plot(data, filename=self.__values_filename, auto_open=False)

    def draw_local_errors(self):
        """
        Create a graph of local errors (data is given by the instance of class Calculator)
        """
        x = self.calculator.x
        errors = self.calculator.get_local_errors()

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
        plotly.offline.plot(data, filename=self.__local_errors_filename, auto_open=False)

    """
    Create a graph of global errors (data is given by the instance of class Calculator)
    """

    def draw_global_errors(self):
        x = self.calculator.global_errors_x
        errors = self.calculator.get_global_errors()

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
        plotly.offline.plot(data, filename=self.__global_errors_filename, auto_open=False)
