import cv2


def closing(binary, kernel, iterations):
    result = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    return result
