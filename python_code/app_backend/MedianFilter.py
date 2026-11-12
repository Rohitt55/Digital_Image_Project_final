import cv2
from OperationRegistry import operation, field


KERNEL = [field('kernel', 'Kernel size (odd)', 5, 3, 31)]

@operation(
    'median',
    'Median filter',
    'Filters & restoration',
    'Reduce impulse noise by selecting the neighborhood median.',
    's(x,y) = median of k × k neighborhood',
    'MedianFilter.py',
    KERNEL
)
def median(image, params, reference):
    return cv2.medianBlur(image, params['kernel'])
