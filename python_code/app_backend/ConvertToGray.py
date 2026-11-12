import cv2


def gray(image):
    if image.ndim == 3:
        result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        result = image
    return result
