import cv2
from OperationRegistry import operation, field


KERNEL = [field('kernel', 'Kernel size (odd)', 5, 3, 31)]

@operation(
    'gaussian',
    'Gaussian filter',
    'Filters & restoration',
    'Smooth using a Gaussian weighted neighborhood.',
    'G(x,y) ∝ exp(-(x²+y²) / (2σ²))',
    'GaussianFilter.py',
    KERNEL
)
def gaussian(image, params, reference):
    return cv2.GaussianBlur(image, (params['kernel'], params['kernel']), 0)
