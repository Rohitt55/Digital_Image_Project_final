import numpy as np


def log_mapping(values):
    transformed = 255 * np.log1p(values) / np.log(256)
    return transformed
