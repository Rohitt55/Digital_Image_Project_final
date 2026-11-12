import numpy as np
from OperationRegistry import operation
from ConvertToGray import gray


@operation(
    'equalize',
    'Normalized equalization',
    'Histograms',
    'Subtract the first nonzero CDF to distribute grayscale values over the full range.',
    's = round((CDF - CDFmin) / (N - CDFmin) × 255)',
    'NormalizedHistEqualization.py'
)
def equalize(image, params, reference):
    values = gray(image)
    hist = np.bincount(values.ravel(), minlength=256)
    cdf = np.cumsum(hist)
    first = cdf[cdf > 0][0]
    if values.size == first:
        return values.copy()

    # Subtract the first nonzero CDF before scaling.
    scaled = (cdf - first) / (values.size - first) * 255
    rounded = np.round(scaled)
    mapping = np.clip(rounded, 0, 255).astype(np.uint8)
    result = mapping[values]
    return result
