import cv2
from OperationRegistry import operation, field


KERNEL = [field('kernel', 'Kernel size (odd)', 5, 3, 31)]

@operation(
    'mean',
    'Average filter',
    'Filters & restoration',
    'Smooth the image by averaging neighboring pixels.',
    's(x,y) = mean of k × k neighborhood',
    'AverageFilter.py',
    KERNEL
)
def mean(image, params, reference):
    return cv2.blur(image, (params['kernel'], params['kernel']))
