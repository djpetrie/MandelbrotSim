"""
This module provides a terminal interface for the user, allowing them to interact with the Mandelbrot simulation using
commands.
@author David Petrie
"""

import random
import sys
from mandelbrot import show, interactive_mandelbrot

# List of POI (point of interest) objects, containing data necessary to recreate a particular view
samples = []    # TODO: change the sample POIs to a text file to allow for saving/loading


def main():
    """
    Provides a terminal user interface for the Mandelbrot simulation, prompting the user for input. Allows the user to
    generate images of the Mandelbrot set, or launch interactive mode.
    :return: None
    """
    print("Initializing Mandelbrot Simulation")
    initialize_samples()
    print("Input \'help\' for command list")
    while True:
        sys.stdout.write(">> ")
        cmd = input()
        if cmd == 'quit':
            print("quitting")
            exit(0)
        elif cmd == 'help':
            str1 = (""
                    "help           provides the command list\n"
                    "interactive    initiates interactive mode\n"
                    "quit           quits the program\n"
                    "tour           displays an image of the Mandelbrot set using a predefined sample point\n")
            print(str1)
        elif cmd == 'interactive':
            print("Engaging interactive mode")
            interactive_mandelbrot()
        elif cmd == 'tour':
            if len(samples) > 0:
                display(samples[random.randint(0, len(samples) - 1)])
            else:
                print("The loaded sample point list is empty")


def initialize_samples():
    """
    Populates a list of POI (point of interest) objects with predefined data.
    :return: None
    """
    samples.append(POI(-1.7693831791955150, 0.0042368479187367, 3.0 / 2.0 ** 39, 1000, 2000))
    samples.append(POI(-0.01759, 0.64456, 3.0 / 2.0 ** 12, 1500, 3000))
    samples.append(POI(-0.759856, 0.125547, 3.0 / 2.0 ** 6, 1500, 600))


def display(sample):
    """
    Displays an image of the Mandelbrot set using the data associated with the given POI (point of interest) object.
    :param sample: A POI object containing the data necessary to recreate a particular view of the mandelbrot set
    :return: None
    """
    show(sample.x_coord, sample.y_coord, sample.field_size, sample.resolution, sample.num_iterations)


class POI:
    """
    This object represents a particular point of interest on the mandelbrot set. The data contained within it's fields
    allow for the view to be reconstructed.
    """
    def __init__(self, x_coord, y_coord, field_size, resolution, num_iterations):
        """
        Contains the fields for this POI
        :param x_coord: X coordinate for the center of the viewing window
        :param y_coord: Y coordinate for the center of the viewing window
        :param field_size: Length in the x-y plane to use for the width of the viewing window
        :param resolution: Number of sample points along the length of the viewing window, total is the square of this
        :param num_iterations: Number of iterations to run for the breakout algorithm on each sample point
        """
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.field_size = field_size
        self.resolution = resolution
        self.num_iterations = num_iterations


if __name__ == '__main__':
    main()
