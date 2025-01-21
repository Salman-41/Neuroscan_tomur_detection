import numpy as np

def inject_noise(image, mean=0, std=0.1):
    """
    Inject Gaussian noise into an image.

    Parameters
    ----------
    image : numpy.ndarray
        The input image with values normalized between 0 and 1.
    mean : float, optional
        The mean of the Gaussian distribution used to generate noise.
    std : float, optional
        The standard deviation of the Gaussian distribution used to generate noise.

    Returns
    -------
    numpy.ndarray
        The noisy image, clipped to [0, 1].
    """
    noise = np.random.normal(mean, std, image.shape)
    noisy_image = image + noise
    return np.clip(noisy_image, 0, 1) #0 (black) 1 (white)


