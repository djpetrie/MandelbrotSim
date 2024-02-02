"""
Contains logic to load the Mandelbrot C library and aid in interfacing with other python modules
@author: David Petrie
"""
import ctypes
from ctypes import c_double, c_int, CDLL

# Pathname
lib_path = './MandelbrotLib.so'
try:
    mandelbrot_lib = CDLL(lib_path)
except FileNotFoundError:
    print('Mandelbrot function library not found')
    exit(1)

# Assigning temporary names to C library functions
python_c_MandelbrotFunction = mandelbrot_lib.MandelbrotFunction
python_c_MandelbrotFunction.restype = ctypes.POINTER(c_int)

python_c_freeMem = mandelbrot_lib.freeMem
python_c_freeMem.restype = None


def mandelbrot_c(x_center, y_center, size, density, num_iterations):
    """
    Returns the data for a view of the Mandelbrot set specified by the given parameters. The Data is returned as a
    ctypes pointer to int, and contains the number of iterations before breakout for each point sampled from the set.
    The calculations are done by calling the C libraries custom algorithm.
    :param x_center: X coordinate for the center of the viewing window
    :param y_center: Y coordinate for the center of the viewing window
    :param size: The length/width of the viewing window in the x-y plane
    :param density: The number of sample points across the length/width of the viewing window
    :param num_iterations: The number of iterations of the breakout algorithm to run on each sample point
    :return: ctypes pointer to int, pointing to an array containing the data for the viewing window
    """
    return python_c_MandelbrotFunction(c_double(x_center), c_double(y_center), c_double(size), c_int(density),
                                       c_int(num_iterations))


def free(ptr):
    """
    Free's the memory that was dynamically allocated in the C libraries MandelbrotFunction
    :param ptr: A pointer to the memory that is to be freed
    :return: None
    """
    python_c_freeMem(ctypes.cast(ptr, ctypes.c_void_p))
