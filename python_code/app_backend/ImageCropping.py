from OperationRegistry import operation, field


@operation(
    'crop',
    'Crop image',
    'Geometry',
    'Specify a rectangle as percentages of the original dimensions.',
    'output = image[y : y+h, x : x+w]',
    'ImageCropping.py',
    [
        field('x', 'Left (%)', 10, 0, 99),
        field('y', 'Top (%)', 10, 0, 99),
        field('width', 'Width (%)', 80, 1, 100),
        field('height', 'Height (%)', 80, 1, 100)
    ]
)
def crop(image, params, reference):
    if params['x'] + params['width'] > 100 or params['y'] + params['height'] > 100:
        raise ValueError('The crop rectangle must fit within the image (left + width and top + height ≤ 100).')
    h, w = image.shape[:2]
    x, y = (int(w * params['x'] / 100), int(h * params['y'] / 100))
    right = min(w, max(x + 1, int(w * (params['x'] + params['width']) / 100)))
    bottom = min(h, max(y + 1, int(h * (params['y'] + params['height']) / 100)))
    return image[y:bottom, x:right].copy()
