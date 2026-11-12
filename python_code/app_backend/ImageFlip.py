import cv2
from OperationRegistry import operation, choice


@operation(
    'flip',
    'Flip image',
    'Geometry',
    'Reflect pixels horizontally, vertically or along both axes.',
    'Horizontal: f(x,y) → f(W-1-x,y)',
    'ImageFlip.py',
    [choice('axis', 'Direction', 'horizontal', ['horizontal', 'vertical', 'both'])]
)
def flip(image, params, reference):
    return cv2.flip(image, {'horizontal': 1, 'vertical': 0, 'both': -1}[params['axis']])
