import numpy as np
# import matplotlib.pyplot as plt
# import random
from scipy.io import wavfile
# import sounddevice as sd

def infosource(signal_type,f,fs,amp,T):
    """Generate a signal based on `signal_type` ('sine' or 'sinc').
    Returns only the time-domain signal m_t.
    """
    if signal_type == "sine":
        start_time = 0
        stop_time = 1
        t = np.linspace((start_time+T), (stop_time+T), int(fs * (stop_time - start_time)) + 1)
        m_t = amp * np.sin(2 * np.pi * f * t)
             

    elif signal_type == 'multitone':
        f_1=f
        f_2 = 2 * f_1
        f_max = max(f_1, f_2)
        fs = 10 * f_max
        start_time = 0
        stop_time = 1
        A_1 = 1
        A_2 = 1
        t = np.linspace(start_time+T, stop_time+T, int(fs * (stop_time - start_time)) + 1)

        m_t = A_1 * np.sin(2 * np.pi * f_1 * t) + A_2 * np.sin(2 * np.pi * f_2 * t)
       
    elif signal_type == "charname":
        name = "Pranav"
        bit_rate = f if f else 1
        dt = 1 / bit_rate
        bits_list = []
        for character in name:
            ascii_value = ord(character)
            binary_string = format(ascii_value, "08b")
            bits_list.extend(int(bit) for bit in binary_string)
        bits = np.array(bits_list, dtype=int)
        t = np.arange(bits.size) * dt + T
        m_t = bits

    elif signal_type == "sinc":
        
        start_time = 0
        stop_time = 1
        t = np.linspace(start_time+T, stop_time+T, int(fs * (stop_time - start_time)) + 1)
        m_t =  2 * f * np.sinc(2 * f* (t+0.5))  # Shifted to center the main lobe within the interval
        

    elif signal_type == "real_time_song":
        fs, m_t = wavfile.read("waving.wav")

        if m_t.ndim > 1:
            m_t = m_t.mean(axis=1)

        if np.issubdtype(m_t.dtype, np.integer):
            max_val = np.iinfo(m_t.dtype).max
            m_t = m_t.astype(np.float64) / max_val
        else:
            m_t = m_t.astype(np.float64)

        t = np.arange(len(m_t)) / fs + T

    elif signal_type == "dial_tone":
        f1 = 350
        f2 = 440
        f_max = max(f1, f2)
        fs = 10 * f_max
        start_time = 0
        stop_time = 1
        A_1 = 1
        A_2 = 1
        t = np.linspace((start_time+T), (stop_time+T), int(fs * (stop_time - start_time)) + 1)
        m_t = m_t = A_1 * np.sin(2 * np.pi * f1 * t) + A_2 * np.sin(2 * np.pi * f2 * t)


       
    else:
        raise ValueError("Unsupported signal type: choose 'sine' or 'sinc'.")

    if signal_type == "charname":
        return bits, t

    return m_t, t
