"""
Contains methods for configuring and plotting images from 2D arrays for use with the mandelbrot program
@author: David Petrie
"""
import matplotlib.pyplot as plt


def setup_figure():
    """
    Sets up the figure and axes for plotting
    :return: The figure and axes
    """
    fig1 = plt.figure(figsize=(10, 10))
    ax1 = fig1.gca()
    fig1.tight_layout()
    ax1.clear()  # clear axes object
    ax1.set_xticks([], [])  # clear x-axis ticks
    ax1.set_yticks([], [])  # clear y-axis ticks
    return fig1, ax1


def image_display(image_data, save=False, plot=True):
    """
    Returns an image of the Mandelbrot set generated from the given image_data, with interpolation and color-mapping.
    The image can be displayed or saved locally via the parameters.
    :param image_data: The 2D array of values used to assign colors to the pixels
    :param save: A boolean to determine if the image is saved locally, false by default
    :param plot: A boolean to determine if the image is shown, true by default
    :return: The image generated
    """

    fig, ax = setup_figure()
    image = plt.imshow(image_data, interpolation="bicubic", cmap='magma')
    if plot:
        plt.show()
    if save:
        fig.savefig("savedImages/test.png")
    return image
