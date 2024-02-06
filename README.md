# Mandelbrot Fractal Simulation

Tools for viewing and exploring fractal images of the Mandelbrot set. 

## Description

A Python 3.10.10 program designed to allow the user to easily generate fractal images of the Mandelbrot set. It provides a basic terminal interface for inputting commands, and provides some sample views that generate images based on recorded parameters.
The user can launch "interactive mode" from the terminal, allowing them to traverse the Mandelbrot set interactively with mouse and keyboard input.

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
