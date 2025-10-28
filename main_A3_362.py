
from plot_time import plot_time
from infosource import infosource
from spectrum_signal import spectrum_signal
from filter_sinc import filter_sinc
from convo_out import convo_out
from txmod import txmod 
from rxdemod import rxdemod
import channel
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.io import wavfile

def main():
    for T in range(1):
        amp=1
        f=80
        fc = 100
        fs, m_t = wavfile.read("waving.wav")
        if m_t.ndim > 1:
            m_t = m_t[:, 0]
        t = np.arange(len(m_t)) / fs + T


        print(len(m_t))
        plot_time(t,m_t)
        # plt.savefig("real_time_song_input.png")
        # plt.pause(2)

        x_t=txmod("FM",m_t,fc,t)      
        # plot_time(t,x_t)
        # plt.pause(2)

        recovered = rxdemod("EDFM", x_t, fc, fs, f, t)
        plot_time(t, recovered)
        plt.savefig("rts_recovered_after_FM_EDFM.png")

    plt.show()   


#   amp = 1
#   bit_rate = 2
#   fs = 100
#   bits, bit_time = infosource("charname", bit_rate, fs, amp, 0)

#   if bits.size == 0:
#       raise ValueError("No bits generated for transmission.")

#   pulse_fs = 1000
#   bit_duration = 1 / bit_rate
#   samples_per_bit = int(pulse_fs * bit_duration)
#   if samples_per_bit <= 1:
#       raise ValueError("Increase pulse sampling rate or reduce bit rate for adequate samples per bit.")

#   dt = 1 / pulse_fs
#   t_pulse = np.arange(samples_per_bit) * dt
#   pulse_bandwidth = bit_rate / 2

#   plt.ion()
#   fig, ax = plt.subplots()
#   cumulative_time = []
#   cumulative_signal = []

#   for index, bit in enumerate(bits):
#       pulse = txmod("polar", bit, pulse_bandwidth, t_pulse)
#       bit_time_axis = index * bit_duration + t_pulse

#       cumulative_time.append(bit_time_axis)
#       cumulative_signal.append(pulse)

#       ax.clear()
#       ax.plot(np.concatenate(cumulative_time), np.concatenate(cumulative_signal))
#       ax.set_title("Polar Modulated Sinc Pulses")
#       ax.set_xlabel("Time [s]")
#       ax.set_ylabel("Amplitude")
#       ax.grid(True)
#       plt.pause(0.2)

#   plt.ioff()
#   plt.show()

if __name__ == "__main__":
    main()
