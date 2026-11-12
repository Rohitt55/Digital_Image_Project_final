import numpy as np
from OperationRegistry import operation
from ConvertToGray import gray


@operation(
    'equalize_basic',
    'Basic histogram equalization',
    'Histograms',
    'Apply the cumulative probability mapping from the basic lab.',
    's = round(255 × CDF(r))',
    'BasicHistEqualization.py'
)
def equalize_basic(image, params, reference):
    values = gray(image)

    # Histogram and cumulative pixel counts.
    hist = np.bincount(values.ravel(), minlength=256)
    cumulative = np.cumsum(hist)

    # Map each original pixel to its equalized intensity.
    scaled = 255 * cumulative / values.size
    mapping = np.round(scaled).astype(np.uint8)
    result = mapping[values]
    return result
