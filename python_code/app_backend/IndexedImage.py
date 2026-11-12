import cv2
import numpy as np
from OperationRegistry import operation, field, choice


@operation('indexed_image', 'Indexed image and color palette', 'Fundamentals',
           'Display the PDF index matrix with its black, red, green and blue palette, or index an uploaded grayscale image.', 'RGB(x,y) = palette[index(x,y)]', 'DIP-Lab1.pdf',
           [choice('input', 'Input', 'PDF matrix', ['PDF matrix', 'Uploaded image'])], requires_reference=False)
def indexed_image(image, params, reference):
    input_mode = params['input']
    if input_mode == 'PDF matrix':
        indexed = np.array([[0, 1, 1, 2], [2, 3, 1, 0], [1, 2, 3, 3], [0, 1, 2, 3]], dtype=np.uint8)
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        indexed = (gray.astype(np.uint16) * 4 // 256).astype(np.uint8)
    palette = np.array([[0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255]], dtype=np.uint8)
    rgb = palette[indexed]
    result = rgb[:, :, ::-1].copy()
    details = {'index_matrix': indexed.tolist() if indexed.size <= 256 else None,
               'palette_rgb': palette.tolist(), 'input': input_mode}
    return result, details
