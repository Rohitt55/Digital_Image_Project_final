import numpy as np
from OperationRegistry import operation, choice
from ConvertToGray import gray


@operation(
    'quantization',
    'Intensity quantization',
    'Color & intensity',
    'Reduce grayscale or per-channel RGB intensity levels to demonstrate digital image quantization.',
    'q = floor(r × levels / 256); s = round(q × 255 / (levels - 1))',
    'DIP-Lab1.pdf',
    [
        choice('bits', 'Bit depth', '3', ['1', '2', '3', '4', '5', '6', '7', '8']),
        choice('domain','Quantization domain','grayscale',['grayscale','RGB channels'])
    ]
)
def quantization(image, params, reference):
    if params['domain'] == 'grayscale':
        values = gray(image)
    else:
        values = image
    values = values.astype(float)

    # Assign each pixel to one of the selected intensity levels.
    levels = 2 ** int(params['bits'])
    indices = np.floor(values * levels / 256)
    quantized = np.round(indices * 255 / (levels - 1))
    result = quantized.astype(np.uint8)
    details = {'intensity_levels': levels}
    return result, details
