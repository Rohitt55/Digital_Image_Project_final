import cv2
import numpy as np
from OperationRegistry import operation, field, choice


@operation('adaptive_mean', 'Adaptive mean threshold', 'Edges & segmentation',
           'Threshold using the local arithmetic mean minus a constant.', 'T(x,y) = mean(local neighborhood) - C', 'DIP-Lab2.pdf',
           [field('kernel', 'Block size (odd)', 11, 3, 51, 1), field('constant', 'Subtracted constant', 2, -30, 30, 1)], requires_reference=False)
def adaptive_mean(image, params, reference):
    kernel = params['kernel']
    constant = params['constant']
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, kernel, constant)
    details = {'foreground_pixels': int(np.count_nonzero(result)), 'background_pixels': int(result.size - np.count_nonzero(result))}
    return result, details
