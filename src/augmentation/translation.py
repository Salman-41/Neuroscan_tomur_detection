import cv2
import numpy as np

def translate_image(image, x, y):
    """
    Args:
      image: The input image as a NumPy array.
      x: The amount of translation in the x-direction (horizontal).
         Positive values translate the image to the right, 
         negative values to the left.
      y: The amount of translation in the y-direction (vertical).
         Positive values translate the image down, 
         negative values up.
    """
    M = np.float32([[1, 0, x], [0, 1, y]])  # Create the translation matrix
    translated = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return translated

    
'''
def translate_image(image, x, y):: This line defines a function called translate_image. It takes three arguments:

    image: The image to be translated.
    x: The amount of translation in the x-direction (horizontal). Positive values translate the image to the right, negative values to the left.
    y: The amount of translation in the y-direction (vertical). Positive values translate the image down, negative values up.

M = np.float32([[1, 0, x], [0, 1, y]]): This line creates a translation matrix M. This matrix defines how much the image needs to be translated.

    np.float32 creates a matrix of floating-point numbers.
    [[1, 0, x], [0, 1, y]] is the translation matrix. This matrix represents a translation in the x and y directions.
    [1, 0, x]: The first row handles horizontal shifts. 1 signifies "preserve x-coordinate," 0 means "no vertical change," and x is the horizontal translation amount.
    [0, 1, y]: Similarly, this row manages vertical shifts. 0 for horizontal, 1 for vertical preservation, and y is the vertical translation amount.


translated = cv2.warpAffine(image, M, (image.shape[1], image.shape[0])): This line uses the cv2.warpAffine function to apply the translation to the image.

    image: The input image.
    M: The translation matrix.
    (image.shape[1], image.shape[0]): The new size of the translated image. This is important to ensure the image is correctly sized after translation.

'''