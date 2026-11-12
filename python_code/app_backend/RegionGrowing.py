import cv2
import numpy as np
from OperationRegistry import operation, field, choice


@operation('region_growing', 'Seed-based Region Growing', 'Edges & segmentation',
           'Analyze at most a 512-pixel side. Grow a 4-connected region whose grayscale values differ from the selected seed by at most the threshold.', 'Accept 4-connected pixels where |gray - seed_intensity| <= tolerance', 'DIP-Lab2.pdf',
           [field('seed_x', 'Seed X (%)', 50, 0, 100, 1), field('seed_y', 'Seed Y (%)', 50, 0, 100, 1), field('tolerance', 'Seed intensity tolerance', 15, 0, 255, 1)], requires_reference=False)
def region_growing(image, params, reference):
    seed_x = params['seed_x']
    seed_y = params['seed_y']
    tolerance = params['tolerance']
    h0, w0 = image.shape[:2]
    scale = min(1.0, 512 / max(h0, w0))
    analysis = cv2.resize(image, (max(1, round(w0 * scale)), max(1, round(h0 * scale))), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(analysis, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    sx = min(w - 1, int(w * seed_x / 100))
    sy = min(h - 1, int(h * seed_y / 100))
    seed_value = int(gray[sy, sx])
    result = np.zeros_like(gray)
    visited = np.zeros_like(gray, dtype=bool)
    stack = [(sx, sy)]
    while stack:
        x, y = stack.pop()
        if x < 0 or x >= w or y < 0 or y >= h or visited[y, x]:
            continue
        visited[y, x] = True
        if abs(int(gray[y, x]) - seed_value) <= tolerance:
            result[y, x] = 255
            stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    details = {'seed_xy': [sx, sy], 'seed_intensity': seed_value,
               'region_pixels': int(np.count_nonzero(result)), 'total_pixels': int(result.size)}
    return result, details
