import cv2


def dilation(binary, kernel, iterations):
    result = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel, iterations=iterations)
    return result
