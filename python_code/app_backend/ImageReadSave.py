import cv2
import numpy as np
import base64
from OperationRegistry import operation, field, choice


@operation('image_read_save', 'Read, display and save image', 'Fundamentals',
           'Read an image and export a PNG copy. The standalone lab writes Results/LabImageCopy.png; the app offers a PNG download.', 'pixels = imread(path); imwrite(output, pixels)', 'DIP-Lab1.pdf',
           [], requires_reference=False)
def image_read_save(image, params, reference):
    result = image.copy()
    ok, encoded = cv2.imencode('.png', result)
    if not ok:
        raise ValueError('Could not encode the image.')
    details = {'width': image.shape[1], 'height': image.shape[0], 'png_bytes': int(encoded.size)}
    details['artifact'] = {'name': 'LabImageCopy.png', 'mime': 'image/png',
                           'data': 'data:image/png;base64,' + base64.b64encode(encoded).decode('ascii')}

    return result, details
