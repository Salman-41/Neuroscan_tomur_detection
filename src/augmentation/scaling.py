import cv2

def scale_image(image, fx, fy):
    """
    Args:
    image: The input image.
    None: This means that the output image size will be calculated based on the scaling factors (fx and fy).
    fx: The scaling factor for the x-axis (horizontal). A value greater than 1 scales the image wider, less than 1 scales it narrower.
    fy: The scaling factor for the y-axis (vertical).
    """
    scaled = cv2.resize(image, None, fx=fx, fy=fy)
    return scaled