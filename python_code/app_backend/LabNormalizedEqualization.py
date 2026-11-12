import cv2
import numpy as np
from OperationRegistry import operation, field, choice


@operation('lab_normalized_equalization', '8x8 normalized histogram equalization', 'Histograms',
           'Use the exact 8x8 intensity matrix from Lab 2 and print its frequency, CDF and mapping table.', 's = round(255 * (cumulative_count(r) - 1) / 63)', 'DIP-Lab2.pdf',
           [], requires_reference=False)
def lab_normalized_equalization(image, params, reference):
    pixels = np.array([
        [52, 55, 61, 59, 79, 61, 76, 61],
        [62, 59, 55, 104, 94, 85, 59, 71],
        [63, 65, 66, 113, 144, 104, 63, 72],
        [64, 70, 70, 126, 154, 109, 71, 69],
        [67, 73, 68, 106, 122, 88, 68, 68],
        [68, 79, 60, 70, 77, 66, 58, 75],
        [69, 85, 64, 58, 55, 61, 65, 83],
        [70, 87, 69, 68, 65, 73, 78, 90]
    ], dtype=np.uint8)
    hist = np.bincount(pixels.ravel(), minlength=256)
    cumulative = np.cumsum(hist)
    cdf_min = int(cumulative[cumulative > 0][0])
    mapped = (cumulative - cdf_min) / (pixels.size - cdf_min) * 255
    mapping = np.clip(np.round(mapped), 0, 255).astype(np.uint8)
    result = mapping[pixels]
    details = {'original_matrix': pixels.tolist(), 'equalized_matrix': result.tolist(),
               'cdf_min': cdf_min, 'total_pixels': int(pixels.size),
               'intensities': np.flatnonzero(hist).tolist(), 'histogram': hist.tolist(),
               'cumulative_counts': cumulative.tolist(), 'mapping': mapping.tolist()}
    return result, details
