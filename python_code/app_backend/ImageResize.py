import cv2
from OperationRegistry import operation, field, choice


@operation(
    'resize',
    'Resize / sampling',
    'Geometry',
    'Choose output dimensions and an interpolation method.',
    'New image = resample(image, width, height)',
    'ImageResize.py',
    [
        field('width', 'Width (px)', 400, 1, 4096),
        field('height', 'Height (px)', 300, 1, 4096),
        choice('interpolation', 'Interpolation', 'area', ['area', 'nearest', 'linear', 'cubic'])
    ]
)
def resize(image, params, reference):
    if params['width'] * params['height'] > 12000000:
        raise ValueError('Output must contain at most 12 million pixels.')
    methods = dict(area=cv2.INTER_AREA, nearest=cv2.INTER_NEAREST, linear=cv2.INTER_LINEAR, cubic=cv2.INTER_CUBIC)
    return cv2.resize(image, (params['width'], params['height']), interpolation=methods[params['interpolation']])
