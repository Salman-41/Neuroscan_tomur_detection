import cv2
import numpy as np

'''Args:
    shear_factor: A positive value shears the image to the right,a negative value shears it to the left.'''
def shear_image(image, shear_factor):
    (h, w) = image.shape[:2]
    '''
    Args:
    1 means no change in the x-direction.
    shear_factor defines how much the image is sheared horizontally.
    0 means no change in the y-direction.
    '''
    M = np.float32([[1, shear_factor, 0], [0, 1, 0]])
    sheared = cv2.warpAffine(image, M, (w, h))
    return sheared


'''def shear_image(image, shear_factor):: This line defines a function called shear_image. It takes two arguments:

    image: The image to be sheared.
    shear_factor: The factor to shear the image horizontally. A positive value shears the image to the right, a negative value shears it to the left.

(h, w) = image.shape[:2]: This line gets the height (h) and width (w) of the image. image.shape tells us the dimensions of the image, and [:2] means we are taking the first two elements, which represent height and width.

M = np.float32([[1, shear_factor, 0], [0, 1, 0]]): This line creates a shear matrix M. This matrix defines how much the image needs to be sheared.

    np.float32 creates a matrix of floating-point numbers.
    [[1, shear_factor, 0], [0, 1, 0]] is the shear matrix. This matrix represents a horizontal shear.
        1 means no change in the x-direction.
        shear_factor defines how much the image is sheared horizontally.
        0 means no change in the y-direction.

sheared = cv2.warpAffine(image, M, (w, h)): This line uses the cv2.warpAffine function to apply the shear to the image.

    image: The input image.
    M: The shear matrix.
    (w, h): The new size of the sheared image.
 '''