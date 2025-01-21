import cv2

def normalize_image(image):
    """
    Normalize an image to the range [0, 255].

    Parameters
    ----------
    image : numpy.ndarray
        The input image to be normalized.

    Returns
    -------
    numpy.ndarray
        The normalized image.
    """
    normalized_image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    return normalized_image
