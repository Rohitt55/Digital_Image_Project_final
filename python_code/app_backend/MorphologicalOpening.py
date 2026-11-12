import cv2


def opening(binary, kernel, iterations):
    result = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=iterations)
    return result
