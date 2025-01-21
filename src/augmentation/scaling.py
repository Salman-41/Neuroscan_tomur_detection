import cv2

def scale_image(image, fx, fy):
    """
    Scale an image along the x and y axes.

    Parameters
    ----------
    image : numpy.ndarray
        The input image to be scaled.
    fx : float
        The scaling factor for the horizontal dimension.
    fy : float
        The scaling factor for the vertical dimension.

    Returns
    -------
    numpy.ndarray
        The scaled image.
    """
    scaled = cv2.resize(image, None, fx=fx, fy=fy)
    return scaled