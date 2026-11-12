import cv2
from OperationRegistry import operation, field
from ConvertToGray import gray


@operation(
    'pixel_matrix',
    'Digital pixel matrix',
    'Geometry',
    'Sample the grayscale image into a small matrix and inspect each pixel value.',
    'Digital image = spatial sampling + intensity quantization',
    'DIP-Lab1.pdf',
    [field('size', 'Matrix size', 8, 2, 16)]
)
def pixel_matrix(image, params, reference):
    values = gray(image)
    size = params['size']
    sampled = cv2.resize(values, (size, size), interpolation=cv2.INTER_AREA)
    details = {'pixel_matrix': sampled.tolist()}
    return sampled, details
