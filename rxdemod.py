import numpy as np
import matplotlib.pyplot as plt
import random
from filter_sinc import filter_sinc
from scipy.signal import convolve, hilbert
from convo_out import convo_out
from txmod import get_last_polar_payload

_last_detection = None


def get_last_detection():
    return _last_detection

def rxdemod(demod_scheme, x_t, fc, fs, f, t):
    global _last_detection
    if demod_scheme == "SD":
        A = 1
        e_t = 2 * x_t * np.cos(2 * np.pi * fc * t) + A * np.cos(2 * np.pi * fc * t)
        recovered = convo_out(e_t, filter_sinc(f, fs))
        _last_detection = None
    elif demod_scheme == "ED":
        analytic = hilbert(x_t)
        envelope = np.abs(analytic)
        envelope_dc = envelope - np.mean(envelope)
        recovered = convo_out(envelope_dc, filter_sinc(f, fs))
        _last_detection = None
    elif demod_scheme == "EDFM":
        analytic = hilbert(x_t)
        phase = np.unwrap(np.angle(analytic))
        dt = t[1] - t[0]
        inst_freq = np.gradient(phase, dt)
        kf = 2 * np.pi * 0.5
        recovered = (inst_freq - 2 * np.pi * fc) / kf
        recovered = convo_out(recovered, filter_sinc(f, fs))
        _last_detection = None
    elif demod_scheme == "th detection":
        payload = get_last_polar_payload()
        if payload is None:
            raise ValueError("polar modulation metadata not available for threshold detection")
        bits_tx = payload["bits"]
        decision_indices = payload["decision_indices"]
        x_array = np.asarray(x_t).flatten()
        valid_mask = (decision_indices >= 0) & (decision_indices < x_array.size)
        samples = np.zeros(decision_indices.size, dtype=float)
        samples[valid_mask] = x_array[decision_indices[valid_mask]]
        detected_bits = (samples > 0).astype(int)
        bit_errors = int(np.sum(bits_tx != detected_bits))
        chars = []
        for start in range(0, detected_bits.size, 8):
            chunk = detected_bits[start:start + 8]
            if chunk.size == 8:
                value = int("".join(str(int(b)) for b in chunk), 2)
                chars.append(chr(value))
        recovered_name = "".join(chars)
        _last_detection = {
            "transmitted_bits": bits_tx,
            "detected_bits": detected_bits,
            "bit_errors": bit_errors,
            "recovered_name": recovered_name,
        }
        return detected_bits
    else:
        raise ValueError("Unsupported demodulation scheme")
    
    
    return recovered

