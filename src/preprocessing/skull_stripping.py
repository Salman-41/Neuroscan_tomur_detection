import cv2
import numpy as np

def skull_strip(image):
    """
    Perform skull stripping on an image to remove non-brain tissues.

    Parameters
    ----------
    image : numpy.ndarray
        The input image to be skull stripped.

    Returns
    -------
    numpy.ndarray
        The skull-stripped image.

    Raises
    ------
    ValueError
        If no contours are found in the image.
    """
    # Ensure the image is in grayscale format
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        raise ValueError("No contours found in the image.")
    
    largest_contour = max(contours, key=cv2.contourArea)
    mask = np.zeros_like(image)
    cv2.drawContours(mask, [largest_contour], -1, 255, cv2.FILLED)
    skull_stripped_image = cv2.bitwise_and(image, image, mask=mask)
    return skull_stripped_image

