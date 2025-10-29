import numpy as np


def pcm_adc(m_t, fs, bits_per_sample, v_min=None, v_max=None):

    samples = np.asarray(m_t, dtype=float)

    levels = 1 << bits_per_sample
    step = (v_max - v_min) / levels

    indices = np.floor((samples - v_min) / step).astype(int)
    indices = np.clip(indices, 0, levels - 1)

    reconstruction = v_min + (indices + 0.5) * step

    bit_masks = 1 << np.arange(bits_per_sample - 1, -1, -1)
    bits = ((indices[:, None] & bit_masks) > 0).astype(np.uint8)
    bitstream = bits.reshape(-1)

    return bitstream, reconstruction, indices


__all__ = ["pcm_adc", "dm_adc"]
