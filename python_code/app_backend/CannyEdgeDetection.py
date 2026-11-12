import cv2
from OperationRegistry import operation, field
from ConvertToGray import gray


@operation(
    'canny',
    'Canny edges',
    'Edges & segmentation',
    'Find thin edges with Gaussian smoothing and hysteresis thresholds.',
    'Smooth → gradients → suppression → hysteresis',
    'CannyEdgeDetection.py',
    [field('low', 'Lower threshold', 100, 0, 255), field('high', 'Upper threshold', 200, 0, 255)]
)
def canny(image, params, reference):
    low = params['low']
    high = params['high']
    if low >= high:
        raise ValueError('The lower threshold must be smaller than the upper threshold.')

    values = gray(image)
    blurred = cv2.GaussianBlur(values, (5, 5), 0)
    result = cv2.Canny(blurred, low, high)
    return result
