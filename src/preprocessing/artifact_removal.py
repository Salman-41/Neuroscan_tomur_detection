
import cv2
import numpy as np
import logging

def remove_artifacts(image):
    logging.info("Starting artifact removal using Gaussian High-Pass Filter")
    try:
        blurred = cv2.GaussianBlur(image, (21, 21), 0)  # Large kernel for strong smoothing
        high_pass = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)  # Blend original and blurred

        logging.info("Artifact removal with Gaussian High-Pass Filter completed")
        return high_pass
    except Exception as e:
        logging.error(f"Error in artifact removal with Gaussian High-Pass Filter: {str(e)}")
        return image



