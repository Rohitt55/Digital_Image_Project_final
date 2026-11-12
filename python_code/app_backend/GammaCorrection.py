import cv2
import numpy as np
from OperationRegistry import operation, field


@operation(
    'gamma',
    'Gamma correction',
    'Color & intensity',
    'A gamma below 1 brightens midtones; above 1 darkens them.',
    's = 255 × (r / 255)^gamma',
    'Chap2 Image Enhancement.pdf',
    [field('gamma', 'Gamma', .7, .1, 5, .1)]
)
def gamma(image, params, reference):
    # Create a lookup table for all 256 intensity values.
    intensities = np.arange(256) / 255
    corrected = 255 * intensities ** params['gamma']
    table = np.round(corrected).astype(np.uint8)
    result = cv2.LUT(image, table)
    return result
