import numpy as np

# Injects Gaussian noise into an image.
def inject_noise(image, mean=0, std=0.1):
    """
    Args:
      mean: The mean of the Gaussian distribution used to generate noise..
      std: The standard deviation of the Gaussian distribution used to 
           generate noise.
    """
    noise = np.random.normal(mean, std, image.shape)
    noisy_image = image + noise
    return np.clip(noisy_image, 0, 1) #0 (black) 1 (white) 


