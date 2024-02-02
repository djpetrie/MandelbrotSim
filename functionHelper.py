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

# C library functions
python_c_MandelbrotFunction = mandelbrot_lib.MandelbrotFunction
python_c_MandelbrotFunction.restype = ctypes.POINTER(c_int)

python_c_freeMem = mandelbrot_lib.freeMem
python_c_freeMem.restype = None


def mandelbrot_c(x_center, y_center, size, density, num_iterations):
    return python_c_MandelbrotFunction(c_double(x_center), c_double(y_center), c_double(size), c_int(density),
                                       c_int(num_iterations))


def free(ptr):
    python_c_freeMem(ctypes.cast(ptr, ctypes.c_void_p))
