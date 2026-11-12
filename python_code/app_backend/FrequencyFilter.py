import numpy as np
from OperationRegistry import operation, field, choice
from ConvertToGray import gray
from NormalizeImage import normalize


@operation(
    'frequency_filter',
    'Frequency filtering',
    'Transforms & comparison',
    'Filter the centered DFT using a circular low-pass or high-pass mask.',
    'Output = IDFT(DFT(image) × frequency mask)',
    'Chap4-Image Transforms.pdf',
    [
        choice('mode', 'Filter type', 'low-pass', ['low-pass', 'high-pass']),
        field('radius', 'Cutoff (% of smaller dimension)', 10, 1, 50)
    ]
)
def frequency_filter(image, params, reference):
    values = gray(image)
    h, w = values.shape

    # Create a circular mask around the center frequency.
    yy, xx = np.ogrid[:h, :w]
    distance_squared = (xx - w // 2) ** 2 + (yy - h // 2) ** 2
    radius = min(h, w) * params['radius'] / 100
    mask = distance_squared <= radius ** 2
    if params['mode'] == 'high-pass':
        mask = ~mask

    # Filter the spectrum and transform back to image space.
    transformed = np.fft.fft2(values)
    centered = np.fft.fftshift(transformed)
    filtered = centered * mask
    shifted_back = np.fft.ifftshift(filtered)
    output = np.fft.ifft2(shifted_back).real

    if params['mode'] == 'high-pass':
        result = normalize(output)
    else:
        rounded = np.round(output)
        result = np.clip(rounded, 0, 255).astype(np.uint8)
    return result
