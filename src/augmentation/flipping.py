import cv2

def flip_image(image, flip_code):
    """
    Flip an image horizontally, vertically, or both.

    Parameters
    ----------
    image : numpy.ndarray
        The input image to flip.
    flip_code : int
        Flip direction:
            0
                Horizontal (left-right).
            1
                Vertical (top-bottom).
            -1
                Both horizontally and vertically.

    Returns
    -------
    numpy.ndarray
        The flipped image.
    """
    flipped = cv2.flip(image, flip_code)
    return flipped



