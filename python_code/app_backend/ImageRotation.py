import cv2
from OperationRegistry import operation, choice


@operation(
    'rotate',
    'Rotate image',
    'Geometry',
    'Rotate in exact quarter turns without interpolation.',
    '90°, 180° or 270° clockwise rotation',
    'ImageRotation.py',
    [choice('angle', 'Clockwise angle', '90', ['90', '180', '270'])]
)
def rotate(image, params, reference):
    rotations = {'90': cv2.ROTATE_90_CLOCKWISE, '180': cv2.ROTATE_180, '270': cv2.ROTATE_90_COUNTERCLOCKWISE}
    return cv2.rotate(image, rotations[params['angle']])
