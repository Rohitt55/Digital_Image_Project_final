import cv2
import numpy as np
from OperationRegistry import operation, field, choice


@operation('histogram_matching', 'Histogram distribution matching', 'Histograms',
           'Match grayscale cumulative distributions to a reference. This is an additional experiment; the PDF code under this heading performs pixel similarity.', 'mapping(r) = inverse_CDF_reference(CDF_source(r))', 'DIP-Lab2.pdf',
           [], requires_reference=True)
def histogram_matching(image, params, reference):
    if reference is None:
        raise ValueError('Upload a reference image for histogram matching.')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    target = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
    source_hist = np.bincount(gray.ravel(), minlength=256)
    target_hist = np.bincount(target.ravel(), minlength=256)
    source_cdf = np.cumsum(source_hist / gray.size)
    target_cdf = np.cumsum(target_hist / target.size)
    mapping = np.searchsorted(target_cdf, source_cdf, side='left')
    mapping = np.clip(mapping, 0, 255).astype(np.uint8)
    result = mapping[gray]
    matched_cdf = np.cumsum(np.bincount(result.ravel(), minlength=256) / result.size)
    details = {'cdf_distance_before': float(np.mean(np.abs(source_cdf - target_cdf))),
               'cdf_distance_after': float(np.mean(np.abs(matched_cdf - target_cdf))),
               'note': 'Discrete intensity distributions may not admit an exact histogram match.'}
    return result, details
