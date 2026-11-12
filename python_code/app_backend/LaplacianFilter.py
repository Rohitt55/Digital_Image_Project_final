import cv2
import numpy as np
from OperationRegistry import operation, field, choice
from ConvertToGray import gray
from NormalizeImage import normalize
from ConvertToUint8 import u8


SOURCE = 'Chap2 Image Enhancement.pdf'

GROUP = 'Filters & restoration'

@operation('laplacian', 'Laplacian sharpening / edges', GROUP, 'Use the second spatial derivative for edge response or sharpening.', '∇²f = ∂²f/∂x² + ∂²f/∂y²; sharpen = f - amount × ∇²f', SOURCE,
           [
               choice('mode','Output','sharpen',['sharpen','edge magnitude']),
               field('amount','Laplacian amount',.5,.1,3,.1)
           ])
def laplacian(image, params, reference):
    values = gray(image).astype(np.float32)
    response = cv2.Laplacian(values, cv2.CV_32F, ksize=3)

    if params['mode'] == 'edge magnitude':
        magnitude = np.abs(response)
        result = normalize(magnitude)
    else:
        sharpened = values - params['amount'] * response
        result = u8(sharpened)
    return result
