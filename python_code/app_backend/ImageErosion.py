import cv2


def erosion(binary, kernel, iterations):
    result = cv2.morphologyEx(binary, cv2.MORPH_ERODE, kernel, iterations=iterations)
    return result
