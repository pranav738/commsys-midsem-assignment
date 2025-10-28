⛬  Session Summary
   •  Reviewed infosource.py and identified inconsistencies across sources, especially real_time_song, as well as multitone/dial_tone
       sampling overrides and the sinc shift.
   •  Cleaned the WAV branch to produce mono, normalized audio with a consistent timeline.
   •  Flagged FM modulator assumptions (fixed deviation kf, reliance on normalized inputs) and implemented three demodulators:
      synchronous (SD), envelope detection (ED), and FM demodulation via Hilbert-based instantaneous frequency (EDFM).
   •  Suggested manual tests comparing transmitted and recovered signals (time plots, spectra, MSE) to validate each
      modulation/demodulation pair.

