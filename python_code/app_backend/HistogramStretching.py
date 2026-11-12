import numpy as np
from OperationRegistry import operation


@operation(
    'stretch',
    'Contrast stretching',
    'Histograms',
    'Map the darkest and brightest values to 0 and 255. Constant images stay unchanged.',
    's = (r - min) / (max - min) × 255',
    'HistogramStretching.py'
)
def stretch(image, params, reference):
    low = float(image.min())
    high = float(image.max())
    if high == low:
        return image.copy()

    # Map the original intensity range to 0 through 255.
    values = image.astype(float)
    stretched = (values - low) / (high - low) * 255
    result = np.round(stretched).astype(np.uint8)
    return result
