import numpy as np


def inverse_filter(transfer, cutoff):
    inverse = np.divide(
        1,
        transfer,
        out=np.zeros_like(transfer),
        where=np.abs(transfer) >= cutoff
    )
    return inverse
