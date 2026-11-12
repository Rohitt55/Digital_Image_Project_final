import numpy as np


def wiener_filter(transfer, regularization):
    power = np.abs(transfer) ** 2
    inverse = transfer.conj() / (power + regularization)
    return inverse
