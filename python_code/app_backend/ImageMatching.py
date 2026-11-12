import cv2
import numpy as np
from OperationRegistry import operation, field
from ConvertToGray import gray


@operation(
    'matching',
    'Pixel similarity',
    'Transforms & comparison',
    'Compare aligned grayscale pixels with a reference, resized to the source dimensions. This measures pixel agreement, not object recognition.',
    'Similarity = count(|source - reference| ≤ tolerance) / N × 100',
    'ImageMatching.py',
    [field('tolerance', 'Intensity tolerance', 5, 0, 255)]
)
def matching(image, params, reference):
    if reference is None:
        raise ValueError('Upload a reference image for pixel similarity.')
    source = gray(image)
    target = cv2.resize(gray(reference), (source.shape[1], source.shape[0]))
    difference = np.abs(source.astype(np.int16) - target.astype(np.int16))
    similar = int(np.count_nonzero(difference <= params['tolerance']))
    return (difference.astype(np.uint8), {
        'similar_pixels': similar,
        'different_pixels': int(source.size - similar),
        'similarity_percent': round(100 * similar / source.size, 3),
        'note': 'Output is the absolute grayscale difference; black pixels are identical.'
    })
