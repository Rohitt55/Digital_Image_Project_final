import cv2
from OperationRegistry import operation
from ConvertToGray import gray
from NormalizeImage import normalize


@operation(
    'sobel',
    'Sobel edges',
    'Edges & segmentation',
    'Find horizontal and vertical gradients and combine their magnitudes.',
    'Magnitude = sqrt(Gx² + Gy²)',
    'SobelEdgeDetection.py'
)
def sobel(image, params, reference):
    values = gray(image)
    sx = cv2.Sobel(values, cv2.CV_32F, 1, 0, ksize=3)
    sy = cv2.Sobel(values, cv2.CV_32F, 0, 1, ksize=3)
    magnitude = cv2.magnitude(sx, sy)
    result = normalize(magnitude)
    return result
