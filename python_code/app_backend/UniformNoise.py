import numpy as np


def uniform_noise(image, params, rng):
    values = image.astype(float)
    sigma = params['sigma']
    noise = rng.uniform(-np.sqrt(3) * sigma, np.sqrt(3) * sigma, image.shape)
    return noise
