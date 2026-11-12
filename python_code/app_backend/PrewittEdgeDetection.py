import cv2
import numpy as np
from OperationRegistry import operation
from ConvertToGray import gray
from NormalizeImage import normalize


@operation(
    'prewitt',
    'Prewitt edges',
    'Edges & segmentation',
    'Estimate gradients using uniform 3 × 3 derivative masks.',
    'Gx = [-1,0,1; -1,0,1; -1,0,1]; Gy = Gxᵀ',
    'PrewittEdgeDetection.py'
)
def prewitt(image, params, reference):
    values = gray(image)
    kx = np.array([[-1, 0, 1],
                   [-1, 0, 1],
                   [-1, 0, 1]], dtype=np.float32)
    ky = kx.T

    px = cv2.filter2D(values, cv2.CV_32F, kx)
    py = cv2.filter2D(values, cv2.CV_32F, ky)
    magnitude = cv2.magnitude(px, py)
    result = normalize(magnitude)
    return result
