import numpy as np
# import matplotlib.pyplot as plt
from scipy.signal import hilbert
# import random
# from scipy.signal import convolve

def txmod(mod_scheme, m_t, fc, t):
    if mod_scheme == "DSB-SC":
        start_time = 0
        stop_time = 1
        x_t = m_t * np.cos(2 * np.pi * fc * t)
    
    if mod_scheme == "AM":
        start_time = 0
        stop_time = 1
        Ac = m_t / abs(m_t)
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
        kf = 2 * np.pi * 0.5  # Frequency sensitivity (adjust as needed)
        # Integrate m_t with respect to time
        dt = t[1] - t[0]
        integral_mt = np.cumsum(m_t) * dt
        x_t = np.cos(2 * np.pi * fc * t + kf * integral_mt)
    if mod_scheme == "polar":
        if t is None or len(t) == 0:
            raise ValueError("Time vector t is required for polar modulation.")
        bit_array = np.asarray(m_t).astype(int).flatten()
        if bit_array.size != 1:
            raise ValueError("Polar modulation expects a single bit at a time.")
        bit_value = bit_array[0]
        amplitude = 1.0 if bit_value == 1 else -1.0
        bandwidth = fc if fc else 1.0
        if bandwidth <= 0:
            raise ValueError("Parameter fc must be positive for polar modulation.")
        centered_t = t - np.mean(t)
        base_pulse = 2 * bandwidth * np.sinc(2 * bandwidth * centered_t)
        x_t = amplitude * base_pulse
    return x_t















        if mod_scheme == "polar":
        if t is None or len(t) == 0:
            raise ValueError("Time vector t is required for polar modulation.")
        bit_array = np.asarray(m_t).astype(int).flatten()
        if bit_array.size != 1:
            raise ValueError("Polar modulation expects a single bit at a time.")
        bit_value = bit_array[0]
        amplitude = 1.0 if bit_value == 1 else -1.0
        bandwidth = fc if fc else 1.0
        if bandwidth <= 0:
            raise ValueError("Parameter fc must be positive for polar modulation.")
        centered_t = t - np.mean(t)
        base_pulse = 2 * bandwidth * np.sinc(2 * bandwidth * centered_t)
        x_t = amplitude * base_pulse