import numpy as np


def gaussian_noise(image, params, rng):
    values = image.astype(float)
    sigma = params['sigma']
    noise = rng.normal(0, sigma, image.shape)
    return noise
