import cv2

def flip_image(image, flip_code):
    '''
    0: Flips the image horizontally (left-right).
    1: Flips the image vertically (top-bottom).
    -1: Flips the image both horizontally and vertically.
    '''
    flipped = cv2.flip(image, flip_code)
    return flipped

# def flip_image(image_path, save_path):
#     image = cv2.imread(image_path)
#     flipped = cv2.flip(image, 1)
#     cv2.imwrite(save_path, flipped)


