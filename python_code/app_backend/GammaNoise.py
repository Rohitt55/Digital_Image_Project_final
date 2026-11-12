import numpy as np


def gamma_noise(image, params, rng):
    values = image.astype(float)
    sigma = params['sigma']
    noise = rng.gamma(2, sigma / np.sqrt(2), image.shape) - np.sqrt(2) * sigma
    return noise
