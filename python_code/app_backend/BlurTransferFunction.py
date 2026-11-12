import numpy as np


def otf(response, shape):
    kernel = np.zeros(shape, float)
    if response.shape[0] > shape[0] or response.shape[1] > shape[1]:
        raise ValueError('Blur kernel must fit inside the image.')
    kernel[:response.shape[0], :response.shape[1]] = response
    kernel = np.roll(kernel, (-(response.shape[0] // 2), -(response.shape[1] // 2)), axis=(0, 1))
    return np.fft.fft2(kernel)
