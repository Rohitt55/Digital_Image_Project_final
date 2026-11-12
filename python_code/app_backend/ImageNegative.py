from OperationRegistry import operation, choice
from ConvertToGray import gray


@operation(
    'negative',
    'Image negative',
    'Color & intensity',
    'Invert each intensity to highlight darker structures.',
    's = 255 - r',
    'Chap2 Image Enhancement.pdf',
    [choice('domain', 'Negative domain', 'grayscale', ['grayscale', 'RGB channels'])]
)
def negative(image, params, reference):
    if params['domain'] == 'grayscale':
        image = gray(image)
    return 255 - image
