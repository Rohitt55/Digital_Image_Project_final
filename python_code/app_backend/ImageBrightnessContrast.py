import numpy as np
from OperationRegistry import operation, field


@operation(
    'contrast',
    'Brightness & contrast',
    'Color & intensity',
    'Scale intensity and add a brightness offset. Saturate values at the valid range.',
    's = clip(alpha × r + beta, 0, 255)',
    'ImageBrightnessContrast.py',
    [field('alpha', 'Contrast (alpha)', 1.3, 0, 4, .1), field('beta', 'Brightness (beta)', 0, -255, 255)]
)
def contrast(image, params, reference):
    # Use float values so arithmetic cannot overflow uint8.
    values = image.astype(np.float32)
    adjusted = values * params['alpha'] + params['beta']
    clipped = np.clip(adjusted, 0, 255)
    result = clipped.astype(np.uint8)
    return result
