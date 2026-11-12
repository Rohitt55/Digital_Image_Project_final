import cv2


def gradient(binary, kernel, iterations):
    result = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel, iterations=iterations)
    return result
