import cv2
from OperationRegistry import operation
from ConvertToGray import gray


@operation(
    'otsu',
    'Otsu segmentation',
    'Edges & segmentation',
    'Choose the threshold that minimizes within-class variance automatically.',
    'T* = argmin within-class variance',
    'Chap5-Image Segmentation.pdf'
)
def otsu(image, params, reference):
    cutoff, output = cv2.threshold(gray(image), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return (output, {'selected_threshold': cutoff})
