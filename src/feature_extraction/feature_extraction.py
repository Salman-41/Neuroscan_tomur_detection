import cv2
import numpy as np

def extract_histogram(image):
    """Extract color histogram features from an image."""
    histogram = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                             [0, 256, 0, 256, 0, 256])
    return cv2.normalize(histogram, histogram).flatten()

def extract_sift_features(image):
    """Extract SIFT features from an image."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    return keypoints, descriptors

def extract_hog_features(image):
    """Extract HOG features from an image."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hog = cv2.HOGDescriptor()
    h = hog.compute(gray)
    return h.flatten()

# Test code
if __name__ == "__main__":
    # Load an example image
    image = cv2.imread('./volume_1_slice_100_jpg.rf.ede22f04cdff52f80737eaec905f3c15.jpg')
    if image is None:
        print("Image not found.")
    else:
        # Extract and print histogram features
        hist_features = extract_histogram(image)
        print("Histogram Features Length:", len(hist_features))
        
        # Extract and print SIFT features
        kp, des = extract_sift_features(image)
        print("Number of SIFT Keypoints:", len(kp))
        
        # Extract and print HOG features
        hog_features = extract_hog_features(image)
        print("HOG Features Length:", len(hog_features))

        # Draw SIFT keypoints and save the image
        kp_image = cv2.drawKeypoints(image, kp, None)
        cv2.imwrite('sift_keypoints.jpg', kp_image)

        # Save HOG visualization image
        from skimage.feature import hog
        hog_features, hog_image = hog(
            cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
            pixels_per_cell=(16, 16),
            cells_per_block=(2, 2),
            visualize=True,
            feature_vector=True
        )
        hog_image_rescaled = (hog_image * 255).astype(np.uint8)
        cv2.imwrite('hog_visualization.jpg', hog_image_rescaled)
