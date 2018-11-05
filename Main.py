from Calculator import Calculator
from Graph import Plotter

c = Calculator()
p = Plotter(c)
p.draw_values()
p.draw_local_errors()
p.draw_global_errors()

