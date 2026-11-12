import cv2
import numpy as np
from OperationRegistry import operation
from ConvertToGray import gray
from NormalizeImage import normalize


@operation(
    'roberts',
    'Roberts edges',
    'Edges & segmentation',
    'Detect diagonal changes using small 2 × 2 masks.',
    'Gx = [1,0;0,-1]; Gy = [0,1;-1,0]',
    'RobertsEdgeDetection.py'
)
def roberts(image, params, reference):
    values = gray(image)
    kx = np.array([[1, 0], [0, -1]], dtype=np.float32)
    ky = np.array([[0, 1], [-1, 0]], dtype=np.float32)
    gx = cv2.filter2D(values, cv2.CV_32F, kx)
    gy = cv2.filter2D(values, cv2.CV_32F, ky)
    magnitude = cv2.magnitude(gx, gy)
    result = normalize(magnitude)
    return result
