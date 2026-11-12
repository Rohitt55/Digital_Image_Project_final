import cv2
import numpy as np
from OperationRegistry import operation, field, choice


@operation('color_spaces', 'RGB, Gray, HSV, Lab and YCrCb conversion', 'Color & intensity',
           'Convert BGR into the selected color space and inspect its individual channels. Encoded HSV/Lab/YCrCb channels are not RGB display colors.', 'Convert BGR to RGB / Gray / HSV / Lab / YCrCb; inspect numerical channels', 'DIP-Lab1.pdf',
           [choice('space', 'Color space', 'YCrCb', ['RGB', 'Gray', 'HSV', 'Lab', 'YCrCb'])], requires_reference=False)
def color_spaces(image, params, reference):
    space = params['space']
    methods = {'RGB': cv2.COLOR_BGR2RGB, 'Gray': cv2.COLOR_BGR2GRAY,
               'HSV': cv2.COLOR_BGR2HSV, 'Lab': cv2.COLOR_BGR2LAB, 'YCrCb': cv2.COLOR_BGR2YCrCb}
    converted = cv2.cvtColor(image, methods[space])
    # The result is the first numerical channel; lab plots show all channels.
    result = converted.copy() if space == 'Gray' else converted[:, :, 0].copy()
    center = converted[converted.shape[0] // 2, converted.shape[1] // 2]
    details = {'color_space': space, 'center_pixel': center.tolist(),
               'channel_order': {'RGB': ['R', 'G', 'B'], 'Gray': ['Gray'], 'HSV': ['H', 'S', 'V'],
                                 'Lab': ['L', 'a', 'b'], 'YCrCb': ['Y', 'Cr', 'Cb']}[space]}
    return result, details
