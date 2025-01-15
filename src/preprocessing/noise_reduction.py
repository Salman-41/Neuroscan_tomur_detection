import cv2
import numpy as np
import pywt

def has_noise(image, threshold=0.01):
    """
    Determines if the image has significant noise using wavelet-based thresholding.
    Args:
        image (np.ndarray): Input image.
        threshold (float): Noise threshold level.
    Returns:
        bool: True if noise level is above the threshold, otherwise False.
    """
    # Convert image to grayscale if it's not already
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Normalize the image for wavelet processing
    image_float = image.astype(np.float32) / 255.0

    # Perform wavelet decomposition
    coeffs = pywt.wavedec2(image_float, 'db1', level=1)
    
    # Estimate noise by calculating the median of the absolute detail coefficients
    sigma_est = np.median(np.abs(coeffs[-1][0])) / 0.6745  # A robust noise estimation
    return sigma_est > threshold

def reduce_noise(image):
    """
    Applies Non-Local Means denoising to reduce noise in the image.
    Args:
        image (np.ndarray): Input image.
    Returns:
        np.ndarray: Noise-reduced image.
    """
    # Convert to grayscale for consistency
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Check for noise and apply denoising if needed
    if has_noise(image):
        # Apply Non-Local Means denoising
        denoised_image = cv2.fastNlMeansDenoising(image, None, h=10, templateWindowSize=7, searchWindowSize=21)
        return denoised_image
    else:
        return image  # Return original image if noise level is below threshold