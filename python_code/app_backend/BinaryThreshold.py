import cv2
from OperationRegistry import operation, field
from ConvertToGray import gray


@operation(
    'threshold',
    'Binary threshold',
    'Edges & segmentation',
    'Separate pixels into foreground and background using one cutoff.',
    's = 255 if r > T, otherwise 0',
    'Chap5-Image Segmentation.pdf',
    [field('threshold', 'Threshold', 127, 0, 255)]
)
def threshold(image, params, reference):
    values = gray(image)
    cutoff = params['threshold']
    _, result = cv2.threshold(values, cutoff, 255, cv2.THRESH_BINARY)
    return result
