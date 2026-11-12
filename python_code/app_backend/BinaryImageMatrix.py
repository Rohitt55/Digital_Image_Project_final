import cv2
import numpy as np
from OperationRegistry import operation, field, choice


@operation('binary_matrix', 'Binary image matrix', 'Fundamentals',
           'Display the exact binary matrix from Lab 1, independent of the uploaded image.', 'Display the PDF 4x4 matrix with values 0 and 1', 'DIP-Lab1.pdf',
           [], requires_reference=False)
def binary_matrix(image, params, reference):
    pixels = np.array([[0, 1, 0, 0], [1, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]], dtype=np.uint8)
    result = pixels * 255
    details = {'binary_matrix': pixels.tolist(), 'foreground_pixels': int(np.count_nonzero(pixels))}
    return result, details
