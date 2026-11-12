import numpy as np


def rayleigh_noise(image, params, rng):
    values = image.astype(float)
    sigma = params['sigma']
    scale = sigma / np.sqrt((4 - np.pi) / 2)
    noise = rng.rayleigh(scale, image.shape) - scale * np.sqrt(np.pi / 2)
    return noise
