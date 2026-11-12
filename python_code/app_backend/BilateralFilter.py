import cv2
from OperationRegistry import operation, field


@operation(
    'bilateral',
    'Bilateral filter',
    'Filters & restoration',
    'Smooth similar colors while preserving strong boundaries.',
    'Weight = spatial Gaussian × intensity Gaussian',
    'BilateralFilter.py',
    [field('diameter', 'Neighborhood diameter', 9, 3, 15), field('sigma', 'Color / space sigma', 75, 1, 150)]
)
def bilateral(image, params, reference):
    return cv2.bilateralFilter(image, params['diameter'], params['sigma'], params['sigma'])
