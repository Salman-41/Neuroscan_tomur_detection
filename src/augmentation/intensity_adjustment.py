import cv2

def adjust_intensity(image, alpha, beta):
    """
    Args:
      alpha: A scaling factor for the pixel values.  
             A value greater than 1 increases the brightness, 
             a value between 0 and 1 decreases it.
             A value of 1 keeps the original intensity.
      beta: A constant value to be added to each pixel value.
            This can further increase or decrease the brightness.
    """
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted