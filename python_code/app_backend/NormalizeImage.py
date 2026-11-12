import cv2
import numpy as np


def normalize(image):
    scaled = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    result = scaled.astype(np.uint8)
    return result
