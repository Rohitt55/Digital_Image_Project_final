import numpy as np


def inverse_log_mapping(values, strength):
    numerator = np.expm1(strength * values / 255)
    denominator = np.expm1(strength)
    transformed = 255 * numerator / denominator
    return transformed
