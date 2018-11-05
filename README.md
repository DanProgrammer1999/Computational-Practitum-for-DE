# Computational Practitum for Differential Equations course

This project is designed and implemented specifically for the assignment for the differential equations course.

The assignment is as following: 
implement three numerical methods (namely, Euler's, Improved Euler's and Range-Kutta methods) for a given 
differential equation (in my case: `y' = y/x + x/y`). Plot the values for the given initial value problem. 
Calculate and plot two types of errors: local errors and global (maximum) errors.

This project consists of two main classes, and one additional to separate the driver code.
All the parameters for both classes are stored in a config file 'Parameters.ini'.

###`Calculator`

Used to calculate values and errors. For the better readability and management, it is divided into two subclasses, 
each having a separate config section: 

`Values` (config section `VALUES`) and `Errors` (config section `ERRORS`)

There are methods (`get_values`, `get_local_errors`, `get_global_errors`) to provide a simple way to get all the
values, local and global errors by calling just one method. 
Alternatively, it is possible to get individual results for each numerical method and each type of error
(i.e. by doing `calculator.values.euler_method` or `calculator.errors.euler_local()`, for example, 
where `calculator` is an instance of class `Calculator`).

###`Plotter` (config section `PLOTTER`)

Used to plot the data calculated by `Calculator` instance (which has to be passed at initialization).
It has three methods, each of them producing an `html` file (by using `pyplot` library):
- `draw_values` plots the values graph, 
- `draw_local_errors` plots the local errors graph (each point in graph is the difference between 
the exact solution and a numerical method result at this point), and 
- `draw_global_errors` draws a graph of maximum local errors for each method for different grid sizes.

###Config file (`Parameters.ini`)

####`Values`
- `x0`, `y0`: initial values; `x0` is also a start of the interval on which the values are calculated;
- `xf`: end of the interval on which the values are calculated;
- `h`: the grid step.

####`Errors`
- `n_err_steps`: number of different grid sizes for calculating the maximum local errors;
- `err0`, `errf`: start and end of the interval for choosing different grid sizes.

#### `Graph`
- `values_filename`, `local_errors_filename`, `global_errors_filename`: names of files for corresponding plots.
- `values_mode`, `local_errors_mode`, `global_errors_mode`: plot modes for corresponding plots.



