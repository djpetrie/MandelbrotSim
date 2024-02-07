"""
This module contains tools to simulate and explore the Mandelbrot set. Data for a simulation is store in a 2D numpy
array and can be displayed as an image or explored in interactive mode. Interactive mode allows the user to explore
the fractal using their mouse and keyboard.
@author: David Petrie
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import draw, pause
from functionHelper import mandelbrot_c
from functionHelper import free
import drawFromArray
import math
from matplotlib.backend_bases import MouseButton

# Global constants
# Determine the default initial conditions for the simulation
DEFAULT_X = -0.5                            # default x coordinate for the center point
DEFAULT_Y = 0.0                             # default y coordinate for the center point
DEFAULT_SIZE = 3.0                          # default size for the interval to sample from
DEFAULT_RESOLUTION = 1000                   # default sample count for width/height of simulation window
DEFAULT_ITERATIONS = 100                    # default iteration count to use for sampling points

# Global Variables
# Used to maintain the simulation state when in interactive mode
g_x = DEFAULT_X                             # current x coordinate of the center point
g_y = DEFAULT_Y                             # current y coordinate of the center point
g_size = DEFAULT_SIZE                       # current size of the interval to sample from
g_resolution = DEFAULT_RESOLUTION           # current density or resolution of sample points
g_iterations = DEFAULT_ITERATIONS           # current iteration base value to use when sampling points
g_iteration_mult = 1.0                      # current multiplier to iteration count for frame generation


def fast_mandelbrot(x_coord, y_coord, field_size, resolution, num_iterations):
    """
    Generates the array for imaging the Mandelbrot set using a C library with a custom edge tracing algorithm.
    Returns a numpy array where the entries A[x][y] correspond to sample points in the complex plane, shifted and scaled
    for the given center coordinate points and field_size. Values represent the number of iterations before the
    corresponding point exited the Mandelbrot bailout algorithm, while non-divergent points are set to zero.
    :param x_coord: x coordinate for center of sample window
    :param y_coord: y coordinate for center of sample window
    :param field_size: size of the interval to sample points from.
    :param resolution: number of pixels/sample points in single dimension
    :param num_iterations: Maximum number of iterations for the Mandelbrot bailout algorithm
    :return: A 2D numpy array with entries corresponding to number of iterations before bailout for a sample point.
    """
    # Invert y to correct data orientation for display
    data1 = mandelbrot_c(x_coord, -y_coord, field_size, resolution, num_iterations)  # ctypes pointer to int
    np_array = np.ctypeslib.as_array(data1, shape=(resolution, resolution)).copy()   # copy as array in python mem
    free(data1)                                                                      # free dynamic memory
    np_array[0][0] = 1  # fixes a bug in imshow where an empty array input produces erratic behavior
    return np_array


def show(x_coord, y_coord, field_size, resolution, num_iterations):
    """
    Displays an image of the Mandelbrot set for the given parameters
    :param x_coord: x coordinate for center of sample window
    :param y_coord: y coordinate for center of sample window
    :param field_size: size of the interval to sample points from.
    :param resolution: number of pixels/sample points in single dimension
    :param num_iterations: Maximum number of iterations for the Mandelbrot bailout algorithm
    :return: The AxisImage from the plotted figure
    """
    if resolution < 128:
        rtn = str(resolution) + " below resolution minimum of 128"
        raise Exception(rtn)
    if num_iterations < 1:
        rtn = str(num_iterations) + " below num_iterations minimum of 1"
        raise Exception(rtn)
    image_data = fast_mandelbrot(x_coord, y_coord, field_size, resolution, num_iterations)
    return drawFromArray.image_display(image_data)


def mouse_event(event, image):
    """
    While in interactive mode: Re-centers the image around the coordinates of a mouse event, and adjusts the zoom level
    and iteration count based on the type of input.

    Left click = zoom in, increase iterations
    Right click = zoom out, decrease iterations
    Middle click = maintain zoom level, only recenter
    :param event: Mouse event from user input
    :param image: The AxisImage for the plot
    :return: None
    """
    global g_size, g_x, g_y, g_iteration_mult
    dist_per_px = g_size / g_resolution
    p_x = event.xdata                                    # x pos of clicked pixel measure from bottom left
    p_y = g_resolution - event.ydata                     # y pos of clicked pixel measure from bottom left
    # print(p_x, p_y)
    x_shift = p_x - g_resolution / 2                     # number of pixels to move center in x direction
    y_shift = p_y - g_resolution / 2                     # number of pixels to move center in y direction
    g_x = g_x + x_shift * dist_per_px                    # move center, scale pixels to distance in current size
    g_y = g_y + y_shift * dist_per_px
    if event.button is MouseButton.LEFT:
        # print(g_size)
        g_size = g_size / 2.0
        # print(g_size)
        iterations = round(g_iterations * max(round(np.log2(DEFAULT_SIZE / g_size)), 1) * g_iteration_mult)
        # print(iterations)
        image.set_data(fast_mandelbrot(g_x, g_y, g_size, g_resolution, num_iterations=iterations))
        image.autoscale()  # scales the color mapping to the new data in img
        draw(), pause(5e-3)
    if event.button is MouseButton.RIGHT:
        g_size = g_size * 2.0
        iterations = round(g_iterations * max(round(np.log2(DEFAULT_SIZE / g_size)), 1) * g_iteration_mult)
        image.set_data(fast_mandelbrot(g_x, g_y, g_size, g_resolution, num_iterations=iterations))
        image.autoscale()  # scales the color mapping to the new data in img
        draw(), pause(5e-3)
    if event.button is MouseButton.MIDDLE:
        iterations = round(g_iterations * max(round(np.log2(DEFAULT_SIZE / g_size)), 1) * g_iteration_mult)
        image.set_data(fast_mandelbrot(g_x, g_y, g_size, g_resolution, num_iterations=iterations))
        image.autoscale()  # scales the color mapping to the new data in img
        draw(), pause(5e-3)


def key_event(event, image):
    """
    Interactive mode only: Adjusts the iteration count or resolution for the generated image, then redraws the image.
    UP ARROW = increase iterations by 25% (additive)
    DOWN ARROW = decrease iterations by 25% (additive)
    RIGHT ARROW = double current resolution
    LEFT ARROW = half current resolution
    :param event: Key even from user input
    :param image: The AxisImage for the plot
    :return: None
    """
    global g_iteration_mult, g_resolution
    if event.key == "up":
        g_iteration_mult = max(g_iteration_mult + 0.25, 0.25)
    if event.key == "down":
        g_iteration_mult = max(g_iteration_mult - 0.25, 0.25)
    if event.key == "up" or event.key == "down":
        iterations = g_iterations * max(round(np.log2(DEFAULT_SIZE / g_size)), 1)
        iterations_scaled = round(iterations * g_iteration_mult)
        image.set_data(fast_mandelbrot(g_x, g_y, g_size, g_resolution, iterations_scaled))
        image.autoscale()  # scales the color mapping to the new data in img
        draw(), pause(5e-3)
    if event.key == "right":
        g_resolution = math.ceil(g_resolution * 2)
    if event.key == "left":
        g_resolution = math.ceil(max(g_resolution / 2, 128))
    if event.key == "left" or event.key == "right":
        plt.close()
        iterations = g_iterations * max(round(np.log2(DEFAULT_SIZE / g_size)), 1)
        iterations_scaled = round(iterations * g_iteration_mult)
        data = fast_mandelbrot(g_x, g_y, g_size, g_resolution, iterations_scaled)
        image = drawFromArray.image_display(data, plot=False)
        fig = image.figure
        fig.canvas.mpl_connect('button_press_event', lambda event2: mouse_event(event2, image))
        fig.canvas.mpl_connect('key_press_event', lambda event2: key_event(event2, image))
        plt.show()


def interactive_mandelbrot():
    """
    Draws the Mandelbrot set, then activates listening for user mouse and keyboard input, placing the programming in a
    state referred to elsewhere as 'interactive mode'. The plotting window can now be controlled via user mouse or
    keyboard input, as documented in the key_event() and mouse_event() methods.
    :return: None
    """
    # mpl.rcParams['keymap.back'].remove('up')
    # mpl.rcParams['keymap.forward'].remove('down')

    # Reset the global variables if a new instance of interactive_mandelbrot is called
    global g_x, g_y, g_size, g_resolution, g_iterations, g_iteration_mult
    g_x = DEFAULT_X
    g_y = DEFAULT_Y
    g_size = DEFAULT_SIZE
    g_resolution = DEFAULT_RESOLUTION
    g_iterations = DEFAULT_ITERATIONS
    g_iteration_mult = 1.0

    data = fast_mandelbrot(g_x, g_y, g_size, g_resolution, g_iterations)
    image = drawFromArray.image_display(data, plot=False)
    fig = image.figure
    fig.canvas.mpl_connect('button_press_event', lambda event: mouse_event(event, image))
    fig.canvas.mpl_connect('key_press_event', lambda event: key_event(event, image))
    plt.show()
