import cv2

def adjust_intensity(image, alpha, beta):
    """
    Adjust an image's brightness or contrast based on alpha and beta values.

    Parameters
    ----------
    image : numpy.ndarray
        The input image to be adjusted.
    alpha : float
        A scaling factor for pixel values. A value > 1 increases brightness,
        a value < 1 decreases brightness, and a value of 1 keeps it unchanged.
    beta : float
        A constant value added to each pixel, further increasing or decreasing brightness.

    Returns
    -------
    numpy.ndarray
        The intensity-adjusted image.
    """
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted