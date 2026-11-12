import cv2
import numpy as np


def psf(kernel, kind):
    if kind == 'motion':
        response = np.zeros((kernel, kernel))
        response[kernel // 2, :] = 1 / kernel
        return response
    g = cv2.getGaussianKernel(kernel, max(kernel / 6, 0.5))
    response = g @ g.T
    return response
