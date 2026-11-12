import numpy as np
from OperationRegistry import operation
from ConvertToGray import gray


@operation(
    'idft',
    'DFT → IDFT reconstruction',
    'Transforms & comparison',
    'Compute a forward DFT and its inverse to reconstruct the grayscale input.',
    'Reconstruction = real(ifft2(fft2(image)))',
    'Student Task-FFT-DFT-IDFT.pdf'
)
def idft(image, params, reference):
    values = gray(image)
    transformed = np.fft.fft2(values)
    reconstructed = np.fft.ifft2(transformed).real

    difference = reconstructed - values.astype(float)
    mse = float(np.mean(difference ** 2))
    rounded = np.round(reconstructed)
    result = np.clip(rounded, 0, 255).astype(np.uint8)
    details = {'reconstruction_mse': mse}
    return result, details
