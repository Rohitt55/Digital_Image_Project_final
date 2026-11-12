import numpy as np
from ConvertToGray import gray


def statistics(image):
    values = gray(image)
    lo, hi = (int(values.min()), int(values.max()))
    histogram = np.bincount(values.ravel(), minlength=256)
    return dict(
        width=image.shape[1],
        height=image.shape[0],
        channels=1 if image.ndim == 2 else 3,
        min=lo,
        max=hi,
        mean=round(float(values.mean()), 3),
        variance=round(float(values.astype(float).var()), 3),
        standard_deviation=round(float(values.astype(float).std()), 3),
        simple_contrast=hi - lo,
        rms_contrast=round(float(values.astype(float).std()), 3),
        michelson=round((hi - lo) / (hi + lo), 4) if hi + lo else 0,
        histogram=histogram.tolist(),
        cdf=(histogram.cumsum() / values.size).tolist()
    )
