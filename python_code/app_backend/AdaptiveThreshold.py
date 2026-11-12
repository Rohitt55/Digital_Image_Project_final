import cv2
from OperationRegistry import operation, field
from ConvertToGray import gray


@operation(
    'adaptive',
    'Adaptive threshold',
    'Edges & segmentation',
    'Compute a local threshold to handle uneven illumination.',
    'T(x,y) = Gaussian weighted neighborhood mean - C',
    'Chap5-Image Segmentation.pdf',
    [field('kernel', 'Block size (odd)', 11, 3, 51), field('constant', 'Subtracted constant', 2, -30, 30)]
)
def adaptive(image, params, reference):
    return cv2.adaptiveThreshold(
        gray(image),
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        params['kernel'],
        params['constant']
    )
