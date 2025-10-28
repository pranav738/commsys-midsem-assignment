import matplotlib.pyplot as plt


def plot_time(t, m_t):
    duration = float(t[-1] - t[0]) if len(t) > 1 else 0.0

    if duration > 1.5:
        # long signal (e.g. real_time_song) — open a new figure so it doesn't overlay
        plt.figure()
    else:
        # short segments — reuse figure 1 to accumulate segments over iterations
        plt.figure(1)

    plt.plot(t, m_t)
    plt.title("Time-Domain")
    plt.xlabel("Time")
    plt.ylabel("Signal Amplitude")
    plt.grid(True)
