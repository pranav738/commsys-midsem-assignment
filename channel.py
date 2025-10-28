import numpy as np

def distortionless_channel(t, A=1.0, t0=0.0):

    h = np.zeros_like(t)
    idx = np.argmin(np.abs(t - t0))
    h[idx] = A
    return h

def bandlimited_channel(t, B=50.0, fs=None):
    N = 101  # filter length (odd number)
    t_h = np.arange(-N//2, N//2 + 1) / fs
    h = 2 * B * np.sinc(2 * B * t_h)
    return h
