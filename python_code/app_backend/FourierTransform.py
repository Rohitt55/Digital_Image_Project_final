import numpy as np
from OperationRegistry import operation
from ConvertToGray import gray
from NormalizeImage import normalize


@operation(
    'fft',
    'FFT / DFT spectrum',
    'Transforms & comparison',
    'Use FFT to compute the 2D DFT, center zero frequency, then display log magnitude.',
    'Spectrum = log(1 + |fftshift(fft2(image))|)',
    'Student Task-FFT-DFT-IDFT.pdf'
)
def fft(image, params, reference):
    values = gray(image)
    transformed = np.fft.fft2(values)
    centered = np.fft.fftshift(transformed)
    magnitude = np.abs(centered)
    spectrum = np.log1p(magnitude)
    result = normalize(spectrum)
    details = {
        'note': 'FFT computes the DFT efficiently. Output shows normalized log magnitude, not the complex coefficients.'
    }
    return result, details
