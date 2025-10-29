
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
import sounddevice as sd

def main():
    for T in range(1):    # Loop to allow multiple tests/runs
        amp=1
        f=10000
        fs=44100
        fc = 150000  # Carrier frequency
        N = 3

        m_t,t = infosource("real_time_song",f,fs,amp,T=1)     # Real-time song input from infosource.py
        
        play_seconds = None

        x_t=txmod("DSB-SC",m_t,fc,t)                            #Transmitted signal with chosen modulation scheme
        # plot_time(t,x_t)
        # plt.pause(2)

        recovered = rxdemod("SD", x_t, fc, fs, f, t)        #Demodulated signal with chosen demodulation scheme

        # Plot and play recovered signal in segments
        total_samples = len(recovered)
        if play_seconds is not None:
            total_samples = min(total_samples, int(play_seconds * fs))

        segments = int(np.ceil(total_samples / fs)) if total_samples else 0

        for T in range(segments):
            start = T * fs
            end = min((T + 1) * fs, total_samples)
            seg_t = np.arange(start, end) / fs
            seg_y = recovered[start:end]
            plt.figure(2)
            plt.plot(seg_t, seg_y, linewidth=0.8)
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")
            plt.title("Recovered Signal — Time Domain")
            plt.tight_layout()
            plt.show(block=False)
            plt.pause(0.2)
            playback_slice = seg_y.astype(np.float64)
            if np.max(np.abs(playback_slice)) > 0:
                playback_slice = playback_slice / np.max(np.abs(playback_slice))
            sd.play(playback_slice.astype(np.float32), fs)
            sd.wait()

    plt.show()

if __name__ == "__main__":
    main()
