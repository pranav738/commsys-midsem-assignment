import numpy as np
import matplotlib.pyplot as plt
import random
from filter_sinc import filter_sinc
from scipy.signal import convolve, hilbert
from convo_out import convo_out

def rxdemod(demod_scheme, x_t, fc, fs, f, t):
    if demod_scheme == "SD":
        A = 1
        e_t = 2 * x_t * np.cos(2 * np.pi * fc * t) + A * np.cos(2 * np.pi * fc * t)
        recovered = convo_out(e_t, filter_sinc(f, fs))
    elif demod_scheme == "ED":
        analytic = hilbert(x_t)
        envelope = np.abs(analytic)
        envelope_dc = envelope - np.mean(envelope)
        recovered = convo_out(envelope_dc, filter_sinc(f, fs))
    elif demod_scheme == "EDFM":
        analytic = hilbert(x_t)
        phase = np.unwrap(np.angle(analytic))
        dt = t[1] - t[0]
        inst_freq = np.gradient(phase, dt)
        kf = 2 * np.pi * 0.5
        recovered = (inst_freq - 2 * np.pi * fc) / kf
        recovered = convo_out(recovered, filter_sinc(f, fs))
    else:
        raise ValueError("Unsupported demodulation scheme")
    
    
    return recovered

