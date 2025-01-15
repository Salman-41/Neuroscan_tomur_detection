import numpy as np
import cv2

def elastic_transform(image, alpha):
    # Create a random number generator with a seed of None for randomness
    random_state = np.random.RandomState(None)

    # Check if the image is grayscale
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Get the height and width of the image
    height, width = image.shape[:2]

    # Generate random distortions for each pixel in the image
    dx = (random_state.rand(height, width) * 2 - 1) * alpha
    dy = (random_state.rand(height, width) * 2 - 1) * alpha

    # Create a meshgrid of x and y coordinates
    x, y = np.meshgrid(np.arange(width), np.arange(height))

    # Apply the distortions to the coordinates
    map_x = np.float32(x + dx)
    map_y = np.float32(y + dy)

    # Remap the image using the distorted coordinates
    # cv2.BORDER_REFLECT_101: Specifies how to handle pixels outside the image boundaries. 
    #  cv2.INTER_LINEAR: used to calculate the new pixel values 
    deformed = cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)

    if len(image.shape) == 2:
        deformed = cv2.cvtColor(deformed, cv2.COLOR_BGR2GRAY)

    return deformed

'''
np.random.RandomState(None): This creates a random number generator with a seed of None, ensuring randomness.
len(image.shape) == 2: Checks if the image is a grayscale image (single channel).
cv2.cvtColor(image, cv2.COLOR_GRAY2BGR): Converts the grayscale image to a color image (3 channels) so that the transformation can be applied to each channel separately.
shape = image.shape: Get the height and width of the image.
dx and dy: These are random distortions generated for each pixel in the image. The alpha parameter controls the intensity of the distortion.
np.meshgrid: Creates a meshgrid of x and y coordinates to iterate over all pixels.
cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101): This function remaps the image using the distorted coordinates.

    cv2.INTER_LINEAR: This is an interpolation method used to calculate the new pixel values when the coordinates are not integers. It provides a smooth transition between pixels. Other options include cv2.INTER_NEAREST (nearest neighbor interpolation) and cv2.INTER_CUBIC (cubic interpolation).
    cv2.BORDER_REFLECT_101: Specifies how to handle pixels outside the image boundaries. BORDER_REFLECT_101 reflects the image across the edges, creating a mirror-like effect.
'''
'''Okay, imagine you have a picture drawn on a rubber sheet. Now, if you stretch or squish parts of this rubber sheet, the picture on it will also stretch or squish, right? That's what this function does to an image:

    Color Check: If your picture is black and white, it first turns it into a color picture because it's easier to play with colors.

    Making Wiggles: It decides how to wiggle or stretch each part of the picture. It's like deciding where to pull or push on the rubber sheet.

    Moving Pixels: Then, it moves each tiny dot (pixel) in the picture according to those wiggles. If a dot needs to go between other dots, it guesses the color by mixing the colors around it (that's what INTER_LINEAR does).

    Edges: If moving the dots makes some parts go off the edge, it pretends the picture is bigger and reflects the edge like a mirror (BORDER_REFLECT_101).

    Back to Black and White: If your original picture was black and white, it turns the new wiggly picture back to black and white.

So, this function makes your picture look like it's been stretched or squished in funny ways, which can help computers learn to recognize things even when they're not perfect!
'''