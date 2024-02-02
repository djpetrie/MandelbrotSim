"""
This module provides a terminal interface for the user, allowing them to interact with the Mandelbrot simulation using
commands.
"""

import random
import sys
from mandelbrot import show, interactive_mandelbrot


samples = []    # TODO: change the sample POIs to a text file to allow for saving/loading


def main():
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
    samples.append(POI(-1.7693831791955150, 0.0042368479187367, 3.0 / 2.0 ** 39, 1000, 2000))
    samples.append(POI(-0.01759, 0.64456, 3.0 / 2.0 ** 12, 1500, 3000))
    samples.append(POI(-0.759856, 0.125547, 3.0 / 2.0 ** 6, 1500, 600))


def display(sample):
    show(sample.x_coord, sample.y_coord, sample.field_size, sample.resolution, sample.num_iterations)


class POI:
    def __init__(self, x_coord, y_coord, field_size, resolution, num_iterations):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.field_size = field_size
        self.resolution = resolution
        self.num_iterations = num_iterations


if __name__ == '__main__':
    main()
