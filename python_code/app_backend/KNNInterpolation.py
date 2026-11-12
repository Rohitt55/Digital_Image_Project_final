import cv2
import numpy as np
from KNNImageInterpolation import interpolate_image
from OperationRegistry import operation, field, choice


@operation('knn_interpolation', 'Distance-weighted KNN interpolation', 'Fundamentals',
           'Estimate pixels from the K nearest spatial samples using inverse-distance weights. The PDF center value is 25 for K=4.', 'estimate = sum(value_i / distance_i) / sum(1 / distance_i)', 'DIP-Lab1.pdf',
           [choice('input', 'Input', 'PDF matrix', ['PDF matrix', 'Uploaded image', 'Uploaded 8x8 image']), field('neighbors', 'Nearest samples (K)', 4, 1, 9, 1), field('size', 'Output matrix size', 3, 3, 16, 1), field('output_side', 'Image reconstruction side (px)', 512, 32, 512)], requires_reference=False)
def knn_interpolation(image, params, reference):
    input_mode = params['input']
    neighbors = params['neighbors']
    size = params['size']
    if input_mode == 'Uploaded 8x8 image':
        return interpolate_image(image, neighbors, params['output_side'])
    if input_mode == 'PDF matrix':
        pixels = np.array([[10, 20], [30, 40]], dtype=np.uint8)
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        pixels = cv2.resize(gray, (3, 3), interpolation=cv2.INTER_AREA)
    h, w = pixels.shape
    yy, xx = np.mgrid[:h, :w]
    positions = np.column_stack((yy.ravel() / (h - 1), xx.ravel() / (w - 1)))
    values = pixels.ravel().astype(float)
    if neighbors > len(values):
        # The 2x2 PDF example has only four available samples.
        neighbors = len(values)
    interpolated = np.zeros((size, size), dtype=float)
    for y in range(size):
        for x in range(size):
            point = np.array([y / (size - 1), x / (size - 1)])
            distances = np.sqrt(np.sum((positions - point) ** 2, axis=1))
            nearest = np.argsort(distances, kind='stable')[:neighbors]
            if distances[nearest[0]] == 0:
                interpolated[y, x] = values[nearest[0]]
            else:
                weights = 1 / distances[nearest]
                interpolated[y, x] = np.sum(weights * values[nearest]) / weights.sum()
    result = np.clip(np.round(interpolated), 0, 255).astype(np.uint8)
    details = {'source_matrix': pixels.tolist(), 'interpolated_values': interpolated.tolist(),
               'effective_neighbors': neighbors, 'center_value': float(interpolated[size // 2, size // 2])}
    return result, details
