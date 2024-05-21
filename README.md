# Mandelbrot Fractal Simulation

A tool for viewing and exploring fractal images of the Mandelbrot set. 

<img src="/images/Mandelbrot5.png?raw=true" width=75% height=75%>

1                                              |  2                                              | 3
:---------------------------------------------:|:-----------------------------------------------:|:---------------------------------------------:
![Alt text](/images/Mandelbrot4.png?raw=true)  |  ![Alt text](/images/Mandelbrot3.png?raw=true)  |  ![Alt text](/images/Mandelbrot6.png?raw=true)

## Description
The Mandelbrot set is defined as the set of complex numbers c for which the following function does not diverge to infinity when iterated. 
$`f(z) = (z)^2 + c`$ ; $`z = 0`$

This is a Python 3.10.10 program designed to allow the user to easily generate fractal images of the Mandelbrot set. It provides a basic terminal interface for inputting commands, and provides some sample views that generate images based on recorded parameters.
The user can launch "interactive mode" from the terminal, allowing them to traverse the Mandelbrot set interactively with mouse and keyboard input.

### Implemenation Details
Points are colored according to their proximity to the set. Lighter colors corresponding to points that are closer, or in other words, points that take a greater number of iterations to diverge. Points that never diverge within the allowed iteration count are considered to be an element of the Mandelbrot set, and are colored black in order to create a greater visual contrast and give the edge of the set a crisp border. 

As the zoom level of the image increases, a greater number of iterations of the standard algorithm are required to generate clear images. In order to avoid long worst case runtimes, this program uses a custom C library to evaluate the sample points, which implements a type of box checking algorithm based off of Mariani's algorithm. Upon checking the points along the border of a small square region, if that set is completely homogenious, then the interior points of the region may be filled with the same value as the border points. To further optimize for runtime on a single thread, it will precalculate every other point along evenly spaced vertical and horizontal gridlines to avoid recalculating points along shared borders and further reduce the number of points by a factor of two. This may lead to small visual artifacts or inaccuracies in rare cases in exchange for reducing the number of iterations of the main algorithm by up to 91%. Visually excluded features are always less that 10 pixels in size, and connected to the rest of the set across a border by a feature that is at most 1 pixel in size. In practice this algorithm is used for culling the massive number of calculations require for coloring regions that are part of the Mandelbrot set proper. Since those regions run all the way to the maximum iteration count on every point, each pixel can take hundreds or even thousands of times as many calculations to complete as those found elsewhere. 


### Controls
Mouse
- Left click = zoom in x2 (centered on mouse)
- Right click = zoom out x2 (centered on mouse)
- Middle click = recenter around mouse location
Keyboard
- Left arrow key = decrease resolution x2
- Right arrow key = increase resolution x2
- Up arrow key = increase iteration count multiplier
- Down arrow key = decrease iteration count multiplier

## Getting Started

### Dependencies

* numpy, matplotlib

Note: This program uses a custom C library for processing data. The necessary file is the shared object file 'mandelbrotlib.so' which was compiled from the included C source file 'MandelbrotTrace4.c' as such:  
```
gcc -shared -fPIC -O3 -o Mandelbrotlib.so MandelbrotTrace4.c  
```


If the library fails to load, it may be necessary to recompile the shared object file for your machine.

### Executing program

* Run main.py
* Type 'help' into the terminal for a list of available commands
* The command 'interactive' places the program into interactive mode, where it can be controlled via mouse and keyboard using the controls listed above.


## Authors

David Petrie (petrie.david.james@gmail.com)

## Acknowledgments

* The algorithm in the C library is based off of Mariani's algorithm, and modified for better single treaded performance.
