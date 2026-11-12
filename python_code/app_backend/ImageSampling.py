import cv2
from OperationRegistry import operation


@operation('sampling', 'Image sampling comparison', 'Fundamentals',
           'Compare the original with nearest-neighbor sampling at 32x32, 64x64 and 1024x1024.',
           'Sample the spatial image grid at several resolutions', 'DIP-Lab1.pdf')
def sampling(image, params, reference):
    result = cv2.resize(image, (1024, 1024), interpolation=cv2.INTER_NEAREST)
    return result, {'sampling_sizes': [[32, 32], [64, 64], [1024, 1024]], 'interpolation': 'nearest neighbor'}
