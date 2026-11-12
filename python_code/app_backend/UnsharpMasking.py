import cv2
import numpy as np
from OperationRegistry import operation, field


@operation(
    'sharpen',
    'Unsharp masking',
    'Filters & restoration',
    'Add a scaled high frequency residual to sharpen detail.',
    's = r + amount × (r - Gaussian(r))',
    'Chap2 Image Enhancement.pdf',
    [field('amount', 'Sharpening amount', 1, .1, 5, .1)]
)
def sharpen(image, params, reference):
    # Subtract a blurred image to obtain the fine details.
    values = image.astype(float)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    details = values - blurred
    sharpened = values + params['amount'] * details
    result = np.clip(sharpened, 0, 255).astype(np.uint8)
    return result
