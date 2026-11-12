import cv2
import numpy as np
from OperationRegistry import operation, field, choice


@operation('watershed', 'Marker-based Watershed segmentation', 'Edges & segmentation',
           'Find foreground markers with a distance transform, then draw Watershed boundaries in red.', 'Otsu -> opening -> distance markers -> Watershed boundaries', 'DIP-Lab2.pdf',
           [field('fraction', 'Foreground distance fraction', 0.5, 0.1, 0.9, 0.05)], requires_reference=False)
def watershed(image, params, reference):
    fraction = params['fraction']
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), dtype=np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    distance = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, foreground = cv2.threshold(distance, fraction * distance.max(), 255, cv2.THRESH_BINARY)
    foreground = foreground.astype(np.uint8)
    unknown = cv2.subtract(sure_bg, foreground)
    count, markers = cv2.connectedComponents(foreground)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(image.copy(), markers)
    result = image.copy()
    result[markers == -1] = [0, 0, 255]
    details = {'foreground_markers': int(count - 1), 'boundary_pixels': int(np.count_nonzero(markers == -1)),
               'note': 'Uniform or heavily textured images may have no useful foreground markers.'}
    return result, details
