import numpy as np


def speckle_noise(image, params, rng):
    values = image.astype(float)
    sigma = params['sigma']
    noise = values * rng.normal(0, sigma / 255, image.shape)
    return noise
