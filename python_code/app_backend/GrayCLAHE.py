import cv2
from OperationRegistry import operation, field
from ConvertToGray import gray


@operation(
    'clahe',
    'Adaptive equalization · CLAHE',
    'Histograms',
    'Enhance local grayscale contrast while limiting noise amplification.',
    'Local histogram equalization with a clip limit',
    'GrayCLAHE.py',
    [field('clip', 'Clip limit', 2, .1, 40, .1), field('grid', 'Tile grid size', 8, 2, 32)]
)
def clahe(image, params, reference):
    values = gray(image)
    grid = params['grid']
    equalizer = cv2.createCLAHE(clipLimit=params['clip'], tileGridSize=(grid, grid))
    result = equalizer.apply(values)
    return result
