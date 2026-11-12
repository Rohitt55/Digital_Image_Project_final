from OperationRegistry import operation
from ConvertToGray import gray


@operation(
    'grayscale',
    'Grayscale',
    'Color & intensity',
    'Convert color into luminance using weighted RGB channels.',
    'Y = 0.299R + 0.587G + 0.114B',
    'ImageGrayscale.py'
)
def grayscale(image, params, reference):
    return gray(image)
