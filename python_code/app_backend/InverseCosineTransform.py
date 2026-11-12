from scipy import fft


def inverse_dct(coefficients, dimensions):
    if dimensions == '2D':
        reconstructed = fft.idctn(coefficients, type=2, norm='ortho')
    else:
        reconstructed = fft.idct(coefficients, type=2, axis=1, norm='ortho')
    return reconstructed
