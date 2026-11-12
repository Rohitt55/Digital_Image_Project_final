import numpy as np


def salt_pepper_noise(image, params, rng):
    values = image.astype(float)
    sigma = params['sigma']
    selector = rng.random(image.shape[:2])
    result = image.copy()
    result[selector < params['amount'] / 2] = 0
    result[(selector >= params['amount'] / 2) & (selector < params['amount'])] = 255
    noise = result.astype(float) - values
    return noise
