import numpy as np


def exponential_noise(image, params, rng):
    values = image.astype(float)
    sigma = params['sigma']
    noise = rng.exponential(sigma, image.shape) - sigma
    return noise
