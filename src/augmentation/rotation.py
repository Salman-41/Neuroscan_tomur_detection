import cv2
import numpy as np

def rotate_image(image, angle):
    (h, w) = image.shape[:2]  # Get the height and width of the image
    center = (w / 2, h / 2)  # Calculate the center of the image
    
    '''
    Args:
    center: The center point of the image.
    angle: The angle of rotation.
    1.0: This is a scaling factor. We keep it 1.0 to keep the image size the same.
    '''
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    '''
    args:    
    image: The input image.
    M: The rotation matrix.
    (w, h): The new size of the rotated image.
    '''
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated
