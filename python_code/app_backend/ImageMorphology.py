from ImageErosion import erosion
from ImageDilation import dilation
from MorphologicalOpening import opening
from MorphologicalClosing import closing
from MorphologicalGradient import gradient

import cv2
import numpy as np
from OperationRegistry import operation, field, choice
from ConvertToGray import gray


@operation(
    'morphology',
    'Morphological processing',
    'Morphology',
    'Apply a structuring element to a thresholded binary image.',
    'Opening = erode then dilate; closing = dilate then erode',
    'Chap8-Morphological Processing.pdf',
    [
        choice('method', 'Operation', 'opening', ['erosion', 'dilation', 'opening', 'closing', 'gradient']),
        field('kernel', 'Kernel size (odd)', 5, 3, 31),
        field('iterations', 'Iterations', 1, 1, 5),
        field('threshold', 'Binary threshold', 127, 0, 255)
    ]
)
def morphology(image, params, reference):
    values = gray(image)
    _, binary = cv2.threshold(values, params['threshold'], 255, cv2.THRESH_BINARY)
    size = params['kernel']
    kernel = np.ones((size, size), np.uint8)
    iterations = params['iterations']
    method = params['method']
    if method == 'erosion':
        result = erosion(binary, kernel, iterations)
    elif method == 'dilation':
        result = dilation(binary, kernel, iterations)
    elif method == 'opening':
        result = opening(binary, kernel, iterations)
    elif method == 'closing':
        result = closing(binary, kernel, iterations)
    else:
        result = gradient(binary, kernel, iterations)
    return result
