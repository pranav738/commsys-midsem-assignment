import numpy as np


def add_awgn(signal, mean=0.0, variance=1.0):
    signal_array = np.asarray(signal, dtype=float)
    if variance < 0:
        raise ValueError("variance must be non-negative")
    noise = np.random.randn(signal_array.size)
    noisy = signal_array + mean + np.sqrt(variance) * noise
    return noisy.reshape(signal_array.shape)
