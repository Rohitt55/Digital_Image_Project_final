import cv2
import numpy as np
import math
from OperationRegistry import operation, field


@operation(
    'compression',
    'JPEG compression',
    'Transforms & comparison',
    'Encode JPEG at the selected quality, then compare the decoded result. Download saves the actual JPEG.',
    'Lossy JPEG encoding with adjustable quality',
    'Chap7-Image Compression.pdf',
    [field('quality', 'JPEG quality', 80, 1, 100)]
)
def compression(image, params, reference):
    ok, encoded = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, params['quality']])
    if not ok:
        raise ValueError('JPEG compression failed.')
    result = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    # Preserve the exact JPEG bytes; report statistics on its decoded pixels.
    import base64
    payload = 'data:image/jpeg;base64,' + base64.b64encode(encoded).decode('ascii')
    mse = float(np.mean((image.astype(float) - result.astype(float)) ** 2))
    return result, {
        'jpeg_bytes': int(encoded.size),
        'raw_pixel_bytes': int(image.nbytes),
        'raw_to_jpeg_ratio': round(image.nbytes / encoded.size, 2),
        'mse': round(mse, 5),
        'psnr_db': round(10 * math.log10(255 ** 2 / mse), 3) if mse else 'infinity',
        'download': payload
    }
