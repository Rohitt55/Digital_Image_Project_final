import numpy as np


def u8(values):
    # Round and limit the pixel values before converting to uint8.
    rounded = np.round(values)
    clipped = np.clip(rounded, 0, 255)
    result = clipped.astype(np.uint8)
    return result
