import numpy as np


def _find_zero_crossings(data):
    zero_crossings = np.where(np.diff(np.sign(data)))[0]
    return zero_crossings


def split_signals_by_current_sign(current, *signals):
    zero_crossings = _find_zero_crossings(current)
    segments = [np.split(current, zero_crossings + 1)]
    for signal in signals:
        segments.append(np.split(signal, zero_crossings + 1))
    return tuple(segments)
