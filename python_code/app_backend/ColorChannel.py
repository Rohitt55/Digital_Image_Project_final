import cv2
import numpy as np
from OperationRegistry import operation, choice


@operation(
    'color_channel',
    'Color space channels',
    'Color & intensity',
    'Inspect an individual RGB, HSV or Lab channel as a grayscale map. HSV hue is scaled from 0–179 to 0–255 for display.',
    'Convert color space → select channel → display intensity',
    'DIP-Lab1.pdf / Chap3-Color Image Processing.pdf',
    [choice(
        'channel',
        'Channel',
        'HSV hue',
        ['Red', 'Green', 'Blue', 'HSV hue', 'HSV saturation', 'HSV value', 'Lab L', 'Lab a', 'Lab b']
    )]
)
def color_channel(image, params, reference):
    channel = params['channel']

    # OpenCV stores color images in Blue, Green, Red order.
    if channel in ['Red', 'Green', 'Blue']:
        channels = {'Red': 2, 'Green': 1, 'Blue': 0}
        index = channels[channel]
        result = image[:, :, index]
    elif channel.startswith('HSV'):
        values = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        channels = {'HSV hue': 0, 'HSV saturation': 1, 'HSV value': 2}
        index = channels[channel]
        result = values[:, :, index]
        if channel == 'HSV hue':
            # Scale OpenCV hue (0 to 179) for display (0 to 255).
            scaled = np.round(result.astype(float) * 255 / 179)
            result = scaled.astype(np.uint8)
    else:
        values = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        channels = {'Lab L': 0, 'Lab a': 1, 'Lab b': 2}
        index = channels[channel]
        result = values[:, :, index]
    return result
