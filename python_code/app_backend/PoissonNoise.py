import numpy as np


def poisson_noise(image, params, rng):
    values = image.astype(float)
    sigma = params['sigma']
    noise = rng.poisson(values / 255 * params['peak']) / params['peak'] * 255 - values
    return noise
