import cv2
import numpy as np

def shear_image(image, shear_factor):
    """
    Apply horizontal shearing to an image.

    Parameters
    ----------
    image : numpy.ndarray
        The input image to be sheared.
    shear_factor : float
        The factor by which to shear the image. Positive values shear to the right,
        negative values shear to the left.

    Returns
    -------
    numpy.ndarray
        The sheared image.
    """
    (h, w) = image.shape[:2]
    '''
    1 means no change in the x-direction.
    shear_factor defines how much the image is sheared horizontally.
    0 means no change in the y-direction.
    '''
    M = np.float32([[1, shear_factor, 0], [0, 1, 0]])
    sheared = cv2.warpAffine(image, M, (w, h))
    return sheared