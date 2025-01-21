import numpy as np
import cv2

def elastic_transform(image, alpha):
    """
    Apply elastic deformation to an image.

    Parameters
    ----------
    image : numpy.ndarray
        The input image.
    alpha : float
        Magnitude of the distortions.

    Returns
    -------
    numpy.ndarray
        The deformed image.
    """
    # Create a random number generator with a seed of None for randomness
    random_state = np.random.RandomState(None)

    # Check if the image is grayscale
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Get the height and width of the image
    height, width = image.shape[:2]

    # Generate random distortions for each pixel in the image
    dx = (random_state.rand(height, width) * 2 - 1) * alpha
    dy = (random_state.rand(height, width) * 2 - 1) * alpha

    # Create a meshgrid of x and y coordinates
    x, y = np.meshgrid(np.arange(width), np.arange(height))

    # Apply the distortions to the coordinates
    map_x = np.float32(x + dx)
    map_y = np.float32(y + dy)

    # Remap the image using the distorted coordinates
    # cv2.BORDER_REFLECT_101: Specifies how to handle pixels outside the image boundaries. 
    #  cv2.INTER_LINEAR: used to calculate the new pixel values 
    deformed = cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)

    if len(image.shape) == 2:
        deformed = cv2.cvtColor(deformed, cv2.COLOR_BGR2GRAY)

    return deformed
