import cv2
import numpy as np
from OperationRegistry import operation, field, choice


@operation('lab_histogram_matrix', '5x5 histogram matrix', 'Histograms',
           'Use the exact 5x5 matrix in Lab 2, independent of the uploaded image.', 'hist(v) = number of PDF matrix pixels equal to v', 'DIP-Lab2.pdf',
           [], requires_reference=False)
def lab_histogram_matrix(image, params, reference):
    pixels = np.array([[2, 3, 4, 4, 6], [1, 2, 4, 5, 6], [1, 1, 5, 6, 6],
                       [0, 1, 3, 3, 4], [0, 1, 2, 3, 4]], dtype=np.uint8)
    hist = np.bincount(pixels.ravel(), minlength=7)
    result = pixels.copy()
    details = {'pixel_matrix': pixels.tolist(), 'histogram': hist.tolist(), 'total_pixels': int(pixels.size)}
    return result, details
