from scipy import fft


def forward_dct(values, dimensions):
    if dimensions == '2D':
        coefficients = fft.dctn(values, type=2, norm='ortho')
    else:
        coefficients = fft.dct(values, type=2, axis=1, norm='ortho')
    return coefficients
