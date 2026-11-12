import numpy as np
from ForwardCosineTransform import forward_dct
from InverseCosineTransform import inverse_dct
from OperationRegistry import operation, field, choice
from ConvertToGray import gray
from NormalizeImage import normalize
from LimitImageSize import bounded
from ConvertToUint8 import u8


SOURCE='Chap4-Image Transforms.pdf'

GROUP='Transforms & comparison'

@operation(
    'dct',
    'Discrete cosine transform / inverse DCT',
    GROUP,
    'Compute an orthonormal 2D DCT or independent 1D row DCTs, then optionally reconstruct from low-frequency coefficients.',
    'F=DCT(f); reconstruction=IDCT(F)',
    SOURCE,
    [
        choice('dimensions','Transform dimensions','2D',['2D','1D rows']),
        choice('mode','Output','spectrum',['spectrum','reconstruction']),
        field('retain','Retain low frequencies (%)',50,1,100)
    ]
)
def dct(image, params, reference):
    # Convert the input to a grayscale floating-point image.
    small = bounded(image, 1024)
    values = gray(small).astype(float)

    # Calculate either the 2D DCT or a DCT along each row.
    coefficients = forward_dct(values, params['dimensions'])

    # Display the coefficient magnitudes on a logarithmic scale.
    if params['mode'] == 'spectrum':
        magnitude = np.abs(coefficients)
        spectrum = np.log1p(magnitude)
        result = normalize(spectrum)
        details = {'note': 'Log absolute DCT coefficients are normalized for display.'}
        return result, details

    # Keep the selected low-frequency rows and columns.
    h, w = values.shape
    if params['dimensions'] == '1D rows':
        rows = h
    else:
        rows = max(1, round(h * params['retain'] / 100))
    cols = max(1, round(w * params['retain'] / 100))
    retained = np.zeros_like(coefficients)
    retained[:rows, :cols] = coefficients[:rows, :cols]

    # Reconstruct the image using the inverse DCT.
    reconstructed = inverse_dct(retained, params['dimensions'])

    error = values - reconstructed
    mse = float(np.mean(error ** 2))
    result = u8(reconstructed)
    details = {
        'retained_coefficients': rows * cols,
        'total_coefficients': h * w,
        'reconstruction_mse': mse
    }
    return result, details
