import cv2
import numpy as np

def translate_image(image, x, y):
    """
    Translate an image by specified amounts along the x and y axes.

    Parameters
    ----------
    image : numpy.ndarray
        The input image as a NumPy array.
    x : int
        The amount of translation in the x-direction (horizontal).
        Positive values translate the image to the right, negative values to the left.
    y : int
        The amount of translation in the y-direction (vertical).
        Positive values translate the image down, negative values up.

    Returns
    -------
    numpy.ndarray
        The translated image.
    """
    M = np.float32([[1, 0, x], [0, 1, y]])
    translated = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return translated

