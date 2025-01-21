import numpy as np

def random_crop(image, crop_size):
    """
    Crop an image to a random region of the specified size.

    Parameters
    ----------
    image : numpy.ndarray
        The input image to be cropped.
    crop_size : tuple of int
        (height, width) specifying the region to crop.

    Returns
    -------
    numpy.ndarray
        The randomly cropped image.

    Raises
    ------
    ValueError
        If the crop size is larger than the image dimensions.
    """
    h, w = image.shape[:2]
    ch, cw = crop_size

    if h < ch or w < cw:
        raise ValueError("Crop size should be smaller than the image size")

    y = np.random.randint(0, h - ch + 1)
    x = np.random.randint(0, w - cw + 1)

    cropped = image[y:y+ch, x:x+cw]
    return cropped

