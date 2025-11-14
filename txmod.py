import numpy as np
# import matplotlib.pyplot as plt
from scipy.signal import hilbert
# import random
# from scipy.signal import convolve

_last_polar_payload = None


def get_last_polar_payload():
    return _last_polar_payload


def txmod(mod_scheme, m_t, fc, t):
    global _last_polar_payload
    if mod_scheme == "DSB-SC":
        start_time = 0
        stop_time = 1
        x_t = m_t * np.cos(2 * np.pi * fc * t)
    
    if mod_scheme == "AM":
        start_time = 0
        stop_time = 1
        Ac = 1.1*np.max(np.abs(m_t))
        x_t = (m_t + Ac) * np.cos(2 * np.pi * fc * t)

    if mod_scheme == "USSB":
        start_time = 0
        stop_time = 1
        term1 = m_t * np.cos(2 * np.pi * fc * t)
        mh_t = np.imag(hilbert(m_t))
        term2 = mh_t * np.sin(2 * np.pi * fc * t)
        x_t = term1 - term2

    if mod_scheme == "LSSB":
        start_time = 0
        stop_time = 1
        term1 = m_t * np.cos(2 * np.pi * fc * t)
        mh_t = np.imag(hilbert(m_t))
        term2 = mh_t * np.sin(2 * np.pi * fc * t)
        x_t = term1 + term2
    if mod_scheme == "FM":
        start_time = 0
        stop_time = 1
        kf = 2 * np.pi * 1  # Frequency sensitivity (adjust as needed)
        # Integrate m_t with respect to time
        dt = t[1] - t[0]
        integral_mt = np.cumsum(m_t) * dt
        x_t = np.cos(2 * np.pi * fc * t + kf * integral_mt)


    if mod_scheme == "polar":
        bit_array = np.asarray(m_t).astype(int).flatten()
        if bit_array.size == 0:
            raise ValueError("polar modulation requires at least one bit")
        t_array = np.asarray(t, dtype=float).flatten()
        if t_array.size != bit_array.size:
            raise ValueError("time vector must align with bitstream for polar modulation")
        if t_array.size > 1:
            dt = float(np.mean(np.diff(t_array)))
        else:
            dt = 1.0
        start_time = float(t_array[0])
        bandwidth = float(fc) if fc else 1.0
        center_times = start_time + np.arange(bit_array.size) * dt
        x_t = np.zeros_like(t_array, dtype=float)
        for idx, bit in enumerate(bit_array):
            amplitude = 1.0 if bit == 1 else -1.0
            x_t += amplitude * bandwidth * np.sinc(2 * bandwidth * (t_array - center_times[idx]))
        decision_indices = np.array([np.argmin(np.abs(t_array - ct)) for ct in center_times], dtype=int)
        _last_polar_payload = {
            "bits": bit_array,
            "times": t_array,
            "decision_indices": decision_indices,
            "dt": dt,
            "bandwidth": bandwidth,
            "start_time": start_time,
        }
        x_t = x_t.astype(float)
        return x_t

    _last_polar_payload = None
    return x_t